from datetime import datetime
from celery import shared_task
import time
# from ca_camera.models import Wantoitem, Main, Sub, Item_maker
import ca_camera

@shared_task
def camera_form_celery():
    print('処理開始')
    new_item = ca_camera.models.Wantoitem.objects.all().order_by("-id")[0]
    # print('途中１')
    in_keyword,out_keyword = new_item.scraping()
    # print('途中２')
    for main_url,main_list in in_keyword.items():
        ca_camera.models.Main.objects.create(wantoitem=new_item,main_url=main_url,main_title=main_list[0],main_ogp_img=main_list[1])
    for sub_url,sub_list in out_keyword.items():
        ca_camera.models.Sub.objects.create(wantoitem=new_item,sub_url=sub_url,sub_title=sub_list[0],sub_ogp_img=sub_list[1])
    print('処理完了')

@shared_task
def camera_reload_celery(*args):
    reload_items = ca_camera.models.Wantoitem.objects.filter(pk__in=args)
    print(reload_items)
    print('処理開始')
    for item in reload_items:
        ca_camera.models.Main.objects.filter(wantoitem=item).delete()
        ca_camera.models.Sub.objects.filter(wantoitem=item).delete()
        in_keyword,out_keyword = item.scraping()
        for main_url,main_list in in_keyword.items():
            ca_camera.models.Main.objects.create(wantoitem=item,main_url=main_url,main_title=main_list[0],main_ogp_img=main_list[1])
        for sub_url,sub_list in out_keyword.items():
            ca_camera.models.Sub.objects.create(wantoitem=item,sub_url=sub_url,sub_title=sub_list[0],sub_ogp_img=sub_list[1])
        item.save()
        print('singleスクレイピング')
    print('処理完了')

# from ca_lens.models import Wantoitem, Main, Sub, Item_maker
import ca_lens

@shared_task
def lens_form_celery():
    print('処理開始')
    new_item = ca_lens.models.Wantoitem.objects.all().order_by("-id")[0]
    # print('途中１')
    in_keyword,out_keyword = new_item.scraping()
    # print('途中２')
    for main_url,main_list in in_keyword.items():
        ca_lens.models.Main.objects.create(wantoitem=new_item,main_url=main_url,main_title=main_list[0],main_ogp_img=main_list[1])
    for sub_url,sub_list in out_keyword.items():
        ca_lens.models.Sub.objects.create(wantoitem=new_item,sub_url=sub_url,sub_title=sub_list[0],sub_ogp_img=sub_list[1])
    print('処理完了')

@shared_task
def lens_reload_celery(*args):
    reload_items = ca_lens.models.Wantoitem.objects.filter(pk__in=args)
    print('処理開始')
    for item in reload_items:
        ca_lens.models.Main.objects.filter(wantoitem=item).delete()
        ca_lens.models.Sub.objects.filter(wantoitem=item).delete()
        in_keyword,out_keyword = item.scraping()
        for main_url,main_list in in_keyword.items():
            ca_lens.models.Main.objects.create(wantoitem=item,main_url=main_url,main_title=main_list[0],main_ogp_img=main_list[1])
        for sub_url,sub_list in out_keyword.items():
            ca_lens.models.Sub.objects.create(wantoitem=item,sub_url=sub_url,sub_title=sub_list[0],sub_ogp_img=sub_list[1])
        item.save()
        print('singleスクレイピング')
    print('処理完了')

@shared_task
def add(x1, x2):
	time.sleep(10)
	y = x1 + x2
	print('処理完了')
	return y
