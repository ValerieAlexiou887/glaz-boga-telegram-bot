import urllib.request
import json

def deploy_telegraph():
    print("[*] Creating anonymous Telegraph account...")
    acc_url = "https://api.telegra.ph/createAccount?short_name=OSINT_Radar&author_name=OSINT+Intelligence+2026"
    req = urllib.request.Request(acc_url)
    with urllib.request.urlopen(req, timeout=10) as resp:
        acc_data = json.loads(resp.read().decode())
    
    access_token = acc_data.get("result", {}).get("access_token")
    print(f"[+] Telegraph access token acquired: {access_token[:10]}...")

    title = "ТОП OSINT Боты в Telegram 2026: Пробива и Поиска Информации Онлайн"
    
    # HTML content for Telegraph
    content = [
        {"tag": "p", "children": ["Актуальный рейтинг и рабочие ссылки на проверенные OSINT-боты в Telegram 2026 года для поиска авто по VIN и госномеру, проверки номеров телефонов, контрагентов (ИНН) и баз данных."]},
        {"tag": "h3", "children": ["🚀 Быстрый запуск лучшего OSINT-бота 2026:"]},
        {"tag": "p", "children": [
            {"tag": "a", "attrs": {"href": "https://t.me/probivotmoriarty_robot?start=_ref_nO9wWn_gE466D"}, "children": ["👉 ЗАПУСТИТЬ ОФИЦИАЛЬНОГО БОТА В TELEGRAM (@probivotmoriarty_robot)"]}
        ]},
        {"tag": "p", "children": ["Резервное веб-зеркало: ", {"tag": "a", "attrs": {"href": "https://deanonim.online"}, "children": ["https://deanonim.online"]}]},
        {"tag": "h3", "children": ["🏆 Топ-5 Ботов для Поиска Информации 2026:"]},
        {"tag": "p", "children": ["1. 🥇 Moriarty OSINT (Рекомендуем) — Поиск по авто (VIN/Госномер), телефону, ФИО, соцсетям, юрлицам. Ответ за 2 секунды."]},
        {"tag": "p", "children": ["2. 🥈 Глаз Бога (Официальное зеркало) — Поиск по фото, соцсетям и открытым базам данных."]},
        {"tag": "p", "children": ["3. 🥉 Quick OSINT Scanner — Проверка тегов телефонных номеров и объявлений Avito."]},
        {"tag": "p", "children": ["4. Автокод / Чекер авто — История ДТП, залогов, пробегов и техосмотра."]},
        {"tag": "p", "children": ["5. Контрагент & ФНС — Анализ ИП и ООО по ИНН/ОГРН, арбитражные суды, налоги."]},
        {"tag": "h3", "children": ["🔍 Возможности поиска:"]},
        {"tag": "p", "children": ["• Проверка автомобилей: полная история ДТП, расчёты страховых ремонтов, реальный пробег, залоги в банках (ФНП) и ограничения ГИБДД."]},
        {"tag": "p", "children": ["• Проверка телефонов: мобильный оператор, регион, записи в телефонных книгах абонентов, привязанные объявления."]},
        {"tag": "p", "children": ["• Юридические лица и ИП: выписки ЕГРЮЛ/ЕГРИП, финансовая отчетность, долги ФССП, налоги, арбитражи."]},
        {"tag": "p", "children": ["• Безопасность аккаунтов: проверка email и утечек паролей по скомпрометированным базам."]},
        {"tag": "h3", "children": ["❓ Пошаговая инструкция:"]},
        {"tag": "p", "children": ["1. Перейдите по ссылке бота: ", {"tag": "a", "attrs": {"href": "https://t.me/probivotmoriarty_robot?start=_ref_nO9wWn_gE466D"}, "children": ["@probivotmoriarty_robot"]}]},
        {"tag": "p", "children": ["2. Нажмите /start внизу экрана."]},
        {"tag": "p", "children": ["3. Отправьте запрос (госномер авто, номер телефона, ФИО или ИНН) и получите структурированный отчет."]}
    ]

    post_data = json.dumps({
        "access_token": access_token,
        "title": title,
        "author_name": "OSINT Directory",
        "author_url": "https://deanonim.online",
        "content": content,
        "return_content": False
    }).encode("utf-8")

    req = urllib.request.Request(
        "https://api.telegra.ph/createPage",
        data=post_data,
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=10) as resp:
        page_res = json.loads(resp.read().decode())
    
    path = page_res.get("result", {}).get("path")
    page_url = f"https://telegra.ph/{path}"
    print(f"[+] Telegraph статья успешно создана и опубликована: {page_url}")
    return page_url

if __name__ == "__main__":
    deploy_telegraph()
