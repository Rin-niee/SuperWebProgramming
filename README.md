сначала выполняем вручную все задачи celery: 
celery -A car worker --loglevel=info
(celery -A car worker --loglevel=info --pool=threads --concurrency=4)
затем подключаем gunicorn в папке где есть mansge.py, так как так быстрее: 
gunicorn --workers=3 --bind=127.0.0.1:8000 car.wsgi:application
перезагрузка gunicorn: 
sudo systemctl daemon-reload 
sudo systemctl restart gunicorn
перезапуск nginx: 
sudo systemctl restart nginx
