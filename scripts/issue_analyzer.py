#!/usr/bin/env python3
"""
Issue Analysis and Automation Script

This script provides automated analysis and handling of GitHub issues.
It can be run locally or integrated into CI/CD workflows.

Features:
- Analyze issue patterns
- Suggest labels based on content
- Detect duplicates
- Generate statistics
- Recommend actions
"""

import json
import os
import re
import sys
from collections import Counter
from datetime import datetime, timedelta
from typing import Dict, List, Set, Optional

try:
    import requests
except ImportError:
    print("Please install requests: pip install requests")
    sys.exit(1)


class IssueAnalyzer:
    """Analyze and automate issue management."""

    def __init__(self, github_token: Optional[str] = None):
        """Initialize analyzer with GitHub token."""
        self.github_token = github_token or os.environ.get("GITHUB_TOKEN")
        self.session = requests.Session()
        if self.github_token:
            self.session.headers.update({
                "Authorization": f"token {self.github_token}",
                "Accept": "application/vnd.github.v3+json"
            })

    def analyze_issue_content(self, title: str, body: str) -> Dict[str, List[str]]:
        """Analyze issue content and suggest labels."""
        title_lower = title.lower()
        body_lower = (body or "").lower()
        content = f"{title_lower} {body_lower}"

        suggested_labels = []
        priority = None
        component = None

        # Type detection
        if any(word in content for word in ["bug", "error", "exception", "broken", "fail"]):
            suggested_labels.append("bug")
        if any(word in content for word in ["feat", "feature", "enhancement", "add", "new"]):
            suggested_labels.append("enhancement")
        if any(word in content for word in ["doc", "documentation", "readme"]):
            suggested_labels.append("documentation")
        if any(word in content for word in ["security", "vulnerability", "exploit"]):
            suggested_labels.append("security")
        if any(word in content for word in ["performance", "slow", "optimization", "speed"]):
            suggested_labels.append("performance")
        if any(word in content for word in ["refactor", "cleanup", "technical debt"]):
            suggested_labels.append("refactor")

        # Priority detection
        if any(word in content for word in ["urgent", "critical", "blocker", "p0"]):
            priority = "priority:high"
        elif any(word in content for word in ["important", "p1"]):
            priority = "priority:medium"
        elif any(word in content for word in ["minor", "trivial", "p2", "p3"]):
            priority = "priority:low"

        # Component detection
        if any(word in content for word in ["legend ci", "legend-ci", "legend"]):
            component = "component:legend-ci"
        elif any(word in content for word in ["workflow", "ci/cd", "github actions", "pipeline"]):
            component = "component:ci-cd"
        elif any(word in content for word in ["docs/", "documentation", "mkdocs"]):
            component = "component:docs"
        elif any(word in content for word in ["script", "scripts/", "automation"]):
            component = "component:scripts"

        if priority:
            suggested_labels.append(priority)
        if component:
            suggested_labels.append(component)

        return {
            "labels": suggested_labels,
            "confidence": self._calculate_confidence(content, suggested_labels)
        }

    def _calculate_confidence(self, content: str, labels: List[str]) -> float:
        """Calculate confidence score for label suggestions."""
        if not labels:
            return 0.0

        keyword_counts = []
        keywords = {
            "bug": ["bug", "error", "exception", "broken"],
            "enhancement": ["feature", "enhancement", "add"],
            "documentation": ["doc", "documentation", "readme"],
            "security": ["security", "vulnerability"],
            "performance": ["performance", "slow", "optimization"]
        }

        for label in labels:
            label_base = label.split(":")[0]
            if label_base in keywords:
                count = sum(content.count(kw) for kw in keywords[label_base])
                keyword_counts.append(count)

        if not keyword_counts:
            return 0.5

        avg_count = sum(keyword_counts) / len(keyword_counts)
        confidence = min(0.5 + (avg_count * 0.1), 1.0)
        return round(confidence, 2)

    def detect_duplicates(self, issue_title: str, existing_issues: List[Dict]) -> List[Dict]:
        """Detect potential duplicate issues using simple similarity."""
        title_words = set(re.findall(r'\w+', issue_title.lower()))

        duplicates = []
        for issue in existing_issues:
            other_title = issue.get("title", "")
            other_words = set(re.findall(r'\w+', other_title.lower()))

            # Calculate Jaccard similarity
            if title_words and other_words:
                intersection = len(title_words & other_words)
                union = len(title_words | other_words)
                similarity = intersection / union if union > 0 else 0

                if similarity > 0.5:  # 50% similarity threshold
                    duplicates.append({
                        "number": issue.get("number"),
                        "title": other_title,
                        "similarity": round(similarity, 2),
                        "url": issue.get("html_url")
                    })

        return sorted(duplicates, key=lambda x: x["similarity"], reverse=True)

    def analyze_repository(self, owner: str, repo: str) -> Dict:
        """Analyze all issues in a repository."""
        if not self.github_token:
            return {"error": "GitHub token required for repository analysis"}

        issues = self._fetch_issues(owner, repo)

        stats = {
            "total_issues": len(issues),
            "open_issues": sum(1 for i in issues if i["state"] == "open"),
            "closed_issues": sum(1 for i in issues if i["state"] == "closed"),
            "label_distribution": self._analyze_labels(issues),
            "age_distribution": self._analyze_age(issues),
            "stale_issues": self._find_stale_issues(issues),
            "issues_without_labels": [i["number"] for i in issues if not i.get("labels")],
            "issues_without_assignee": [i["number"] for i in issues if not i.get("assignee")]
        }

        return stats

    def _fetch_issues(self, owner: str, repo: str, state: str = "all") -> List[Dict]:
        """Fetch issues from GitHub API."""
        url = f"https://api.github.com/repos/{owner}/{repo}/issues"
        params = {"state": state, "per_page": 100}

        all_issues = []
        page = 1

        while True:
            params["page"] = page
            response = self.session.get(url, params=params)

            if response.status_code != 200:
                print(f"Error fetching issues: {response.status_code}")
                break

            issues = response.json()
            if not issues:
                break

            # Filter out pull requests
            all_issues.extend([i for i in issues if "pull_request" not in i])
            page += 1

            if len(issues) < 100:
                break

        return all_issues

    def _analyze_labels(self, issues: List[Dict]) -> Dict[str, int]:
        """Analyze label distribution."""
        label_counter = Counter()
        for issue in issues:
            for label in issue.get("labels", []):
                label_counter[label["name"]] += 1
        return dict(label_counter.most_common())

    def _analyze_age(self, issues: List[Dict]) -> Dict[str, int]:
        """Analyze issue age distribution."""
        now = datetime.utcnow()
        age_buckets = {
            "< 1 week": 0,
            "1-4 weeks": 0,
            "1-3 months": 0,
            "3-6 months": 0,
            "> 6 months": 0
        }

        for issue in issues:
            if issue["state"] != "open":
                continue

            created = datetime.strptime(issue["created_at"], "%Y-%m-%dT%H:%M:%SZ")
            age = now - created

            if age < timedelta(weeks=1):
                age_buckets["< 1 week"] += 1
            elif age < timedelta(weeks=4):
                age_buckets["1-4 weeks"] += 1
            elif age < timedelta(days=90):
                age_buckets["1-3 months"] += 1
            elif age < timedelta(days=180):
                age_buckets["3-6 months"] += 1
            else:
                age_buckets["> 6 months"] += 1

        return age_buckets

    def _find_stale_issues(self, issues: List[Dict], days: int = 30) -> List[Dict]:
        """Find stale issues (no activity for X days)."""
        now = datetime.utcnow()
        stale_threshold = now - timedelta(days=days)

        stale = []
        for issue in issues:
            if issue["state"] != "open":
                continue

            updated = datetime.strptime(issue["updated_at"], "%Y-%m-%dT%H:%M:%SZ")
            if updated < stale_threshold:
                stale.append({
                    "number": issue["number"],
                    "title": issue["title"],
                    "age_days": (now - updated).days,
                    "url": issue["html_url"]
                })

        return sorted(stale, key=lambda x: x["age_days"], reverse=True)

    def generate_report(self, owner: str, repo: str, output_file: Optional[str] = None) -> str:
        """Generate a comprehensive issue analysis report."""
        stats = self.analyze_repository(owner, repo)

        report = f"""# Issue Analysis Report
Repository: {owner}/{repo}
Generated: {datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")}

## Summary
- Total Issues: {stats['total_issues']}
- Open Issues: {stats['open_issues']}
- Closed Issues: {stats['closed_issues']}

## Label Distribution
"""
        for label, count in list(stats['label_distribution'].items())[:10]:
            report += f"- {label}: {count}\n"

        report += f"""
## Age Distribution (Open Issues)
"""
        for age_range, count in stats['age_distribution'].items():
            report += f"- {age_range}: {count}\n"

        report += f"""
## Issues Needing Attention
- Issues without labels: {len(stats['issues_without_labels'])}
- Issues without assignee: {len(stats['issues_without_assignee'])}
- Stale issues (>30 days): {len(stats['stale_issues'])}

## Top Stale Issues
"""
        for issue in stats['stale_issues'][:5]:
            report += f"- #{issue['number']}: {issue['title']} ({issue['age_days']} days)\n"
            report += f"  {issue['url']}\n"

        if output_file:
            with open(output_file, 'w') as f:
                f.write(report)
            print(f"Report saved to {output_file}")

        return report


def main():
    """Main entry point for CLI usage."""
    import argparse

    parser = argparse.ArgumentParser(description="Analyze GitHub issues")
    parser.add_argument("command", choices=["analyze", "report", "suggest-labels"],
                        help="Command to execute")
    parser.add_argument("--owner", required=True, help="Repository owner")
    parser.add_argument("--repo", required=True, help="Repository name")
    parser.add_argument("--title", help="Issue title (for suggest-labels)")
    parser.add_argument("--body", help="Issue body (for suggest-labels)")
    parser.add_argument("--output", help="Output file for report")

    args = parser.parse_args()

    analyzer = IssueAnalyzer()

    if args.command == "analyze":
        stats = analyzer.analyze_repository(args.owner, args.repo)
        print(json.dumps(stats, indent=2))

    elif args.command == "report":
        report = analyzer.generate_report(args.owner, args.repo, args.output)
        print(report)

    elif args.command == "suggest-labels":
        if not args.title:
            print("Error: --title is required for suggest-labels command")
            sys.exit(1)

        result = analyzer.analyze_issue_content(args.title, args.body or "")
        print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
