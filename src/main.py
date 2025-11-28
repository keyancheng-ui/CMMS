from db import initialize_database
from db.employee_dao import EmployeeDAO
import re
import ast


def parse_input(user_input: str):
    user_input = user_input.strip()
    if not user_input.endswith(')'):
        raise ValueError("格式错误：请以括号结尾，例如 func(...)")

    if '(' not in user_input:
        raise ValueError("格式错误：缺少括号")

    method_name, args_str = user_input.split('(', 1)
    args_str = args_str.rstrip(')')  # 去掉末尾的 )

    if not args_str.strip():
        return method_name.strip(), []

    # 关键：自动给未加引号的“单词”加上引号
    # 匹配：连续的字母、数字、下划线，但不在引号内
    # 简化处理：先把所有内容按逗号分割，再逐个处理
    args_list = []
    for arg in args_str.split(','):
        arg = arg.strip()
        # 如果已经是字符串（以 ' 或 " 开头结尾），保留
        if (arg.startswith("'") and arg.endswith("'")) or \
                (arg.startswith('"') and arg.endswith('"')):
            args_list.append(arg)
        elif arg.isdigit() or (arg.startswith('-') and arg[1:].isdigit()):
            # 是整数
            args_list.append(arg)
        elif re.match(r'^-?\d+\.\d+$', arg):
            # 是浮点数
            args_list.append(arg)
        else:
            # 默认当作字符串，加上单引号
            args_list.append(f"'{arg}'")

    # 拼成一个元组字符串，用 ast.literal_eval 安全解析
    safe_str = f"({', '.join(args_list)},)"
    try:
        parsed = ast.literal_eval(safe_str)
        return method_name.strip(), list(parsed)
    except Exception as e:
        raise ValueError(f"参数解析失败: {e}")



def main():
    print("start to initialize database...")

    # use all default values
    initialize_database(password=input("Input your own mySQL password: "))

    print("database initialization finished")
    print("the system is now ready for use")
    print("this is our Employee related query functions. What do you want to look up?")
    print("get_all_employees(self):\nget_employee_by_ssn(self, ssn):\nadd_employee(self, ssn, name, emp_level):\nget_employees_by_level(self, level):\nupdate_employee(self, ssn, new_level):\ndelete_employee(self, ssn):")
    employee_dao = EmployeeDAO()
    while True:
        try:
            user_input = input(">>> ").strip()
            if user_input.lower() in ('quit', 'exit', 'q'):
                print("再见！")
                break

            if not user_input:
                continue

            method_name, args = parse_input(user_input)

            # 检查方法是否存在
            if not hasattr(employee_dao, method_name):
                print(f"错误：EmployeeDAO 没有方法 '{method_name}'")
                continue

            method = getattr(employee_dao, method_name)

            # 调用方法
            result = method(*args)

            # 打印结果（可根据需要美化）
            if result is None:
                print("操作成功（无返回值）")
            elif isinstance(result, list):
                print(f"返回 {len(result)} 条记录：")
                for item in result:
                    print("  ", item)
            else:
                print("结果：", result)

        except Exception as e:
            print("❌ 错误：", e)

    employee_dao.close()  # 如果你的 DAO 有 close 方法


if __name__ == "__main__":
    main()
