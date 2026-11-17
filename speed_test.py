import time
import sys
import urllib.request
import urllib.error

def measure_speed(url: str, requests_count: int = 10):
    total_time = 0.0
    total_bytes = 0
    successful_requests = 0

    print(f"Начинаем тест для: {url}")
    print(f"Количество запросов: {requests_count}\n")

    for i in range(1, requests_count + 1):
        try:
            # Засекаем время перед запросом
            start_time = time.perf_counter()
            
            # Делаем запрос и читаем весь ответ (дожидаемся полного ответа)
            with urllib.request.urlopen(url) as response:
                data = response.read()
            
            # Засекаем время после полного чтения
            end_time = time.perf_counter()
            
            elapsed = end_time - start_time
            size = len(data)
            
            total_time += elapsed
            total_bytes += size
            successful_requests += 1
            
            print(f"Запрос {i}/{requests_count}: {elapsed:.3f} сек, {size / 1024:.1f} КБ")
            
        except urllib.error.URLError as e:
            print(f"Запрос {i}/{requests_count}: Ошибка - {e.reason}")
        except Exception as e:
            print(f"Запрос {i}/{requests_count}: Неизвестная ошибка - {e}")

    if successful_requests == 0:
        print("\nВсе запросы завершились ошибкой. Невозможно рассчитать скорость.")
        return

    # Расчеты
    avg_time = total_time / successful_requests
    avg_size_bytes = total_bytes / successful_requests
    
    # Скорость в Мегабитах в секунду (Mbps)
    # Байты -> Биты (x8) -> Мегабиты (/ 1_000_000) -> Делим на время в секундах
    speed_mbps = (total_bytes * 8) / (total_time * 1_000_000)

    print("\n" + "="*40)
    print("РЕЗУЛЬТАТЫ ТЕСТА:")
    print("="*40)
    print(f"Успешных запросов: {successful_requests} из {requests_count}")
    print(f"Среднее время запроса: {avg_time:.3f} сек")
    print(f"Средний размер файла: {avg_size_bytes / 1024:.1f} КБ")
    print(f"Общий объем скачанных данных: {total_bytes / (1024*1024):.2f} МБ")
    print(f"Скорость скачивания: {speed_mbps:.2f} Mbps (Мегабит в секунду)")
    print("="*40)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Использование: python speed_test.py <URL>")
        print("Пример: python speed_test.py https://httpbin.org/image/jpeg")
        sys.exit(1)
        
    target_url = sys.argv[1]
    measure_speed(target_url)
