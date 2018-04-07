import csv
import random

last_name = '赵 钱 孙 李 周 吴 郑 王 冯 陈 楚 魏 蒋 沈 韩 杨 万 冼 夏'.split()
first_name1 = '学 习 韩 婷 春 夏 秋 冬 伟 彤 磊 星 晓 羽 邦 项 政'.split()
first_name2 = first_name1 + ['']
def random_students_csv(filename, num):
    with open(filename, 'w', newline='') as csvfile:
        fields = ('id', 'name')
        writer = csv.DictWriter(csvfile, fieldnames=fields)

        writer.writeheader()
        for i in range(num):
            name = random.choice(last_name) \
                   + random.choice(first_name1) \
                   + random.choice(first_name2)
            writer.writerow({'id': str(10000000+i), 'name': name})

if __name__ == '__main__':
    random_students_csv('student_list.csv', 40)
