LOVE = 5201314


def love():
    """打印 9 次“喜欢她”，每 3 次换一行。"""
    for i in range(1, 10):
        print("喜欢她", end=" ")
        if i % 3 == 0:
            print()
    print()  # 收尾换行，避免和后面的输出黏在同一行


# 只有直接运行 python def1.py 时才执行，被 import 时不要产生副作用
if __name__ == "__main__":
    print(LOVE)
    print(__name__)
    love()
