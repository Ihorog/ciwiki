export const greet = (name: string): string => {
  return `Hello, ${name}!`;
};

if (require.main === module) {
  // Example usage
  console.log(greet('World'));
}
