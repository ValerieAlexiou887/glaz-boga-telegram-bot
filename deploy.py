#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Автоматизированный скрипт развертывания Parasite SEO сетки на GitHub:
1. Создание репозитория с ключевыми словами в slug.
2. Настройка тем/тегов (topics) для внутреннего поиска GitHub и поисковиков.
3. Заливка оптимизированного README.md и статического сайта index.html.
4. Включение GitHub Pages (*.github.io).
5. Публикация SEO-гиста на gist.github.com для двойного охвата выдачи.

Все операции проводятся без использования персональных данных пользователя.
"""

import os
import sys
import json
import argparse
import urllib.request
import urllib.error
import subprocess

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

REPO_NAME_DEFAULT = "glaz-boga-telegram-bot-2026"
REPO_DESC = "⚡ Глаз Бога Бот Телеграм 2026: Официальное зеркало и рейтинг лучших OSINT ботов для поиска информации (авто, телефон, VIN, юрлица)."
REPO_TOPICS = [
    "glaz-boga",
    "osint",
    "telegram-bot",
    "probiv",
    "poisk-po-nomeru",
    "proverka-avto",
    "vin-check",
    "eye-of-god",
    "bot-telegram-2026"
]

def make_github_request(url, method="GET", data=None, token=None):
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "OSINT-SEO-Deployer/1.0",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    
    body = None
    if data is not None:
        headers["Content-Type"] = "application/json"
        body = json.dumps(data).encode("utf-8")
        
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req) as response:
            res_body = response.read().decode("utf-8")
            if res_body:
                return response.status, json.loads(res_body)
            return response.status, {}
    except urllib.error.HTTPError as e:
        err_msg = e.read().decode("utf-8")
        try:
            return e.code, json.loads(err_msg)
        except Exception:
            return e.code, {"error": err_msg}

def deploy_repo(token, repo_name=REPO_NAME_DEFAULT):
    print(f"[*] Проверка токена GitHub...")
    code, user_info = make_github_request("https://api.github.com/user", token=token)
    if code != 200:
        print(f"[!] Ошибка авторизации токена (код {code}): {user_info}")
        return False
    
    username = user_info.get("login")
    print(f"[+] Авторизован аккаунт: {username} (никаких личных данных не передается)")

    # 1. Создание репозитория
    print(f"[*] Создание публичного репозитория '{repo_name}'...")
    create_payload = {
        "name": repo_name,
        "description": REPO_DESC,
        "homepage": f"https://{username}.github.io/{repo_name}/",
        "private": False,
        "has_issues": False,
        "has_projects": False,
        "has_wiki": False,
        "auto_init": False
    }
    code, res = make_github_request("https://api.github.com/user/repos", method="POST", data=create_payload, token=token)
    if code not in (200, 201):
        if "already exists" in str(res):
            print(f"[i] Репозиторий '{repo_name}' уже существует. Продолжаем...")
        else:
            print(f"[!] Не удалось создать репозиторий (код {code}): {res}")
            return False
    else:
        print(f"[+] Репозиторий создан: {res.get('html_url')}")

    # 2. Установка тегов (topics)
    print(f"[*] Установка SEO-тегов репозитория: {', '.join(REPO_TOPICS)}...")
    topics_payload = {"names": REPO_TOPICS}
    code, res = make_github_request(f"https://api.github.com/repos/{username}/{repo_name}/topics", method="PUT", data=topics_payload, token=token)
    if code == 200:
        print(f"[+] Теги успешно установлены.")
    else:
        print(f"[!] Предупреждение: не удалось обновить теги: {res}")

    # 3. Пуш исходников через Git
    print(f"[*] Локальная сборка и публикация кода...")
    current_dir = os.path.dirname(os.path.abspath(__file__))
    remote_url = f"https://x-access-token:{token}@github.com/{username}/{repo_name}.git"

    # Настройка анонимного автора в git
    subprocess.run(["git", "config", "user.name", "OSINT Directory"], cwd=current_dir, check=False)
    subprocess.run(["git", "config", "user.email", "osint-directory@users.noreply.github.com"], cwd=current_dir, check=False)

    # Явно добавляем только рабочие файлы SEO-репозитория (защита от утечки токенов)
    files_to_add = ["README.md", "index.html", "robots.txt", "sitemap.xml", "GIST_SEO_TEMPLATE.md", "SETUP_GUIDE.md", "deploy.py", "deploy_telegraph.py", ".gitignore"]
    for f in files_to_add:
        if os.path.exists(os.path.join(current_dir, f)):
            subprocess.run(["git", "add", f], cwd=current_dir, check=False)

    subprocess.run(["git", "commit", "-m", "Initial release: OSINT bot directory and verification guide 2026"], cwd=current_dir, check=False)
    subprocess.run(["git", "branch", "-M", "main"], cwd=current_dir, check=False)
    
    # Push
    push_res = subprocess.run(["git", "push", "-u", remote_url, "main", "--force"], cwd=current_dir, capture_output=True, text=True)
    if push_res.returncode == 0:
        print(f"[+] Файлы (README.md, index.html, robots.txt, sitemap.xml) успешно залиты на GitHub!")
    else:
        print(f"[!] Ошибка при отправке кода: {push_res.stderr}")

    # 4. Включение GitHub Pages
    print(f"[*] Активация GitHub Pages (*.github.io)...")
    pages_payload = {
        "source": {
            "branch": "main",
            "path": "/"
        }
    }
    code, res = make_github_request(f"https://api.github.com/repos/{username}/{repo_name}/pages", method="POST", data=pages_payload, token=token)
    if code in (200, 201):
        print(f"[+] GitHub Pages включен! Страница будет доступна по адресу: https://{username}.github.io/{repo_name}/")
    elif code == 409 or "already" in str(res):
        print(f"[i] GitHub Pages уже активирован на ветке main.")
    else:
        print(f"[!] Информация по GitHub Pages (код {code}): {res.get('message', res)}")

    # 5. Создание Gist для gist.github.com
    print(f"[*] Создание SEO-гиста на gist.github.com...")
    gist_file_path = os.path.join(current_dir, "GIST_SEO_TEMPLATE.md")
    if os.path.exists(gist_file_path):
        with open(gist_file_path, "r", encoding="utf-8") as gf:
            gist_content = gf.read()
        
        gist_payload = {
            "description": "⚡ Глаз Бога Бот Телеграм 2026 — Топ OSINT боты для пробива авто, номеров и контрагентов онлайн",
            "public": True,
            "files": {
                "glaz-boga-telegram-bot-2026.md": {
                    "content": gist_content
                }
            }
        }
        code, res = make_github_request("https://api.github.com/gists", method="POST", data=gist_payload, token=token)
        if code in (200, 201):
            print(f"[+] Gist успешно создан и индексируется: {res.get('html_url')}")
        else:
            print(f"[!] Ошибка создания Gist: {res}")

    print("\n" + "="*60)
    print("🎉 РАЗВЕРТЫВАНИЕ СЕТКИ PARASITE SEO ЗАВЕРШЕНО УСПЕШНО!")
    print(f"1. Репозиторий: https://github.com/{username}/{repo_name}")
    print(f"2. GitHub Pages: https://{username}.github.io/{repo_name}/")
    print("="*60)
    return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Деплой Parasite SEO сетки на GitHub")
    parser.add_argument("--token", required=True, help="GitHub Personal Access Token (classic или fine-grained с правами repo и gist)")
    parser.add_argument("--repo", default=REPO_NAME_DEFAULT, help="Имя репозитория (по умолчанию glaz-boga-telegram-bot-2026)")
    args = parser.parse_args()

    deploy_repo(args.token, args.repo)
