from django.utils import timezone

# 时间戳（假设为秒级时间戳）
timestamp = 1691886651

# 将时间戳转换为 datetime 对象
datetime_obj = timezone.datetime.fromtimestamp(timestamp)

# 将 datetime 对象转换为可读的时间格式
readable_time = datetime_obj.strftime('%Y-%m-%d %H:%M:%S')

print("可读时间:", readable_time)
print(type(readable_time))