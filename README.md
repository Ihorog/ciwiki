# Cimeika Nav Pack

Призначення: застосувати 7 розділів головного меню і повну структуру «Легенда CI» у розділі Казкар.

## Вміст
- `mkdocs.yml` — готова конфігурація навігації.
- `apply_cimeika_nav.sh` — Git Bash-скрипт, що створює гілку, додає заглушки і замінює mkdocs.yml.

## Як використати (Windows, Git Bash)
```bash
cd /c/Users/simei/ciwiki
# Розпакуйте архів сюди (у корінь репозиторію)
chmod +x ./apply_cimeika_nav.sh
./apply_cimeika_nav.sh
```
Потім створіть Pull Request з гілки `content/cimeika-7-sections`.
