from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt

FEEDBACK_STORAGE = []


@csrf_exempt
def calculate_view(request):
    if request.method == "POST":
        n_str = request.POST.get("n", "0")
        
        try:
            n = int(n_str)
            if n < 0:
                n = 0
        except ValueError:
            n = 0

        a, b = 0, 1
        for _ in range(n):
            a, b = b, a + b
        
        return redirect(f"/result/?n={n}&result={a}")
    
    html_form = """
    <!DOCTYPE html>
    <html lang="uk">
    <head>
        <meta charset="UTF-8">
        <title>Обчислення Фібоначчі</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; }
            form { display: flex; flex-direction: column; width: 280px; gap: 10px; }
            input, button { padding: 8px; font-size: 14px; }
        </style>
    </head>
    <body>
        <h2>Обчислення n-го числа Фібоначчі</h2>
        <form action="" method="POST">
            <label>Введіть порядковий номер (n):</label>
            <input type="number" name="n" min="0" required placeholder="Наприклад, 10">
            <button type="submit">Обчислити</button>
        </form>
    </body>
    </html>
    """
    return HttpResponse(html_form)


def result_view(request):
    n = request.GET.get("n", "0")
    result = request.GET.get("result", "0")

    html_content = f"""
    <!DOCTYPE html>
    <html lang="uk">
    <head>
        <meta charset="UTF-8">
        <title>Результат обчислення</title>
        <style>body {{ font-family: Arial, sans-serif; margin: 40px; }}</style>
    </head>
    <body>
        <h2>Результат обчислення Фібоначчі</h2>
        <p>Для порядкового номера <b>n = {n}</b> значення Фібоначчі дорівнює:</p>
        <h3>{result}</h3>
        <br>
        <a href="/calculate/">Повернутися до калькулятора</a>
    </body>
    </html>
    """
    return HttpResponse(html_content)


@csrf_exempt
def feedback_view(request):
    if request.method == "POST":
        name = request.POST.get("name", "Анонім")
        rating = request.POST.get("rating")

        if rating and rating.isdigit():
            rating_val = int(rating)
            if 1 <= rating_val <= 5:
                FEEDBACK_STORAGE.append({"name": name, "rating": rating_val})

        return redirect("/rating/")

    html_form = """
    <!DOCTYPE html>
    <html lang="uk">
    <head>
        <meta charset="UTF-8">
        <title>Форма зворотного зв'язку</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; }
            form { display: flex; flex-direction: column; width: 280px; gap: 10px; }
            input, select, button { padding: 8px; font-size: 14px; }
        </style>
    </head>
    <body>
        <h2>Залишити відгук</h2>
        <form action="" method="POST">
            <label>Ваше ім'я:</label>
            <input type="text" name="name" required placeholder="Введіть ім'я">
            
            <label>Оцінка (від 1 до 5):</label>
            <select name="rating" required>
                <option value="1">1 — Погано</option>
                <option value="2">2 — Задовільно</option>
                <option value="3">3 — Нормально</option>
                <option value="4">4 — Добре</option>
                <option value="5" selected>5 — Відмінно</option>
            </select>
            
            <button type="submit">Надіслати відгук</button>
        </form>
    </body>
    </html>
    """
    return HttpResponse(html_form)



def rating_view(request):
    total_reviews = len(FEEDBACK_STORAGE)

    rating_counts = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
    total_sum = 0

    for item in FEEDBACK_STORAGE:
        r = item["rating"]
        if r in rating_counts:
            rating_counts[r] += 1
            total_sum += r

    avg_rating = round(total_sum / total_reviews, 2) if total_reviews > 0 else 0.0

    html_content = f"""
    <!DOCTYPE html>
    <html lang="uk">
    <head>
        <meta charset="UTF-8">
        <title>Статистика рейтингу</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; }}
            ul {{ list-style-type: none; padding: 0; }}
            li {{ margin-bottom: 5px; }}
        </style>
    </head>
    <body>
        <h2>Статистика відгуків</h2>
        <p><b>Загальна кількість відгуків:</b> {total_reviews}</p>
        <p><b>Середня оцінка:</b> {avg_rating} / 5</p>
        
        <h3>Розподіл оцінок:</h3>
        <ul>
            <li>1 зірка: {rating_counts[1]}</li>
            <li>2 зірки: {rating_counts[2]}</li>
            <li>3 зірки: {rating_counts[3]}</li>
            <li>4 зірки: {rating_counts[4]}</li>
            <li>5 зірок: {rating_counts[5]}</li>
        </ul>
        <br>
        <a href="/feedback/">Залишити ще один відгук</a> | 
        <a href="/calculate/">Перейти до калькулятора</a>
    </body>
    </html>
    """
    return HttpResponse(html_content)