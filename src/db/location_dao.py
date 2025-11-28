from . import DatabaseConnection
from .base_dao import BaseDAO
from .validators import Validators, ensure_not_empty
from typing import Dict, Any, List


class LocationDAO(BaseDAO):

    def create_location(self, building, floor, room_number):

        try:

            ensure_not_empty(building, "building")  # 若为空会直接抛出异常，被后续 except 捕获
            ensure_not_empty(floor, "floor")  # 确保 floor 不为 None（整数类型本身不会空，但防传 None）
            ensure_not_empty(room_number, "room_number")  # 同上

            # 2. 调用自定义验证函数，逐字段校验合法性
            # 建筑物校验
            build_valid, build_msg = Validators.validate_building(building)
            if not build_valid:
                print(build_msg)
                return

            # 楼层校验
            floor_valid, floor_msg = Validators.validate_floor(floor)
            if not floor_valid:
                print(floor_msg)
                return

            # 房号校验（补充类型校验）
            room_valid, room_msg = Validators.validate_room(room_number)
            if not room_valid:
                print(room_msg)
                return


            # 3. 数据库操作（使用 with 语句自动管理连接/游标，避免资源泄露）
            with DatabaseConnection() as db:  # 假设 DatabaseConnection 支持上下文管理器（推荐）
                query = "INSERT INTO Location (Building, Floor, Room_number) VALUES (%s, %s, %s)"
                # 执行 SQL（参数化查询，防止 SQL 注入）
                with db.connection.cursor() as cursor:
                    cursor.execute(query, (building, floor, room_number))
                    db.connection.commit()  # 提交事务，确保数据写入

            # 4. 成功响应：返回插入的完整数据和成功信息
            return {
                "success": True,
                "message": "Location inserted successfully",
                "data": {
                    "Building": building,
                    "Floor": floor,
                    "Room_number": room_number
                }
            }

        except ValueError as ve:
            # 捕获 ensure_not_empty 抛出的空值异常，或其他值错误
            return {"success": False, "error": f"Value error: {str(ve)}"}
        except TypeError as te:
            # 捕获类型错误（如传入非预期类型，且未被前面的类型校验拦截）
            return {"success": False, "error": f"Type error: {str(te)}"}
        except Exception as e:
            # 捕获数据库相关或其他未预期异常（如字段不匹配、连接失败等）
            return {"success": False, "error": f"Database/System error: {str(e)}"}

    def check_location(self, building, floor, room_number) -> Dict[str, Any]:

        try:
            # 1. 先做参数验证（顺序修正：验证通过才查数据库）
            # 基础非空校验（补充字段名，异常信息更清晰）
            ensure_not_empty(building, "building")
            ensure_not_empty(floor, "floor")
            ensure_not_empty(room_number, "room_number")

            # 自定义验证函数（逐字段校验）
            build_valid, build_msg = Validators.validate_building(building)
            if not build_valid:
                return {"success": False, "error": f"Building 验证失败：{build_msg}"}

            floor_valid, floor_msg = Validators.validate_floor(floor)
            if not floor_valid:
                return {"success": False, "error": f"Floor 验证失败：{floor_msg}"}

            room_valid, room_msg = Validators.validate_room(room_number)
            if not room_valid:
                return {"success": False, "error": f"Room_number 验证失败：{room_msg}"}

            # 2. 验证通过，用 with 语句管理数据库资源（自动关闭连接/游标，避免泄露）
            with DatabaseConnection() as db:
                query = "SELECT * FROM Location WHERE Building = %s AND Floor = %s AND Room_number = %s"
                # 用 dictionary=True 返回字典格式结果（方便后续使用，可选）
                with db.connection.cursor(dictionary=True) as cursor:
                    cursor.execute(query, (building, floor, room_number))
                    result = cursor.fetchone()  # 只查一条（存在即返回，效率更高）

            # 3. 处理查询结果（返回统一格式）
            if result:
                message = f"位置存在：建筑物={building}，楼层={floor}，房号={room_number}"
                print(message)
                return {"success": True, "exists": True, "message": message}
            else:
                message = f"位置不存在：建筑物={building}，楼层={floor}，房号={room_number}"
                print(message)
                return {"success": True, "exists": False, "message": message}

        except ValueError as ve:
            # 捕获 ensure_not_empty 抛出的空值异常
            error_msg = f"参数为空：{str(ve)}"
            print(f"查询失败：{error_msg}")
            return {"success": False, "error": error_msg}
        except TypeError as te:
            # 捕获类型错误（比如传入非整数 floor）
            error_msg = f"参数类型错误：{str(te)}"
            print(f"查询失败：{error_msg}")
            return {"success": False, "error": error_msg}
        except Exception as e:
            # 捕获数据库或其他未预期异常
            error_msg = f"数据库/系统错误：{str(e)}"
            print(f"查询失败：{error_msg}")
            return {"success": False, "error": error_msg}

    def get_all_locations(self) -> Dict[str, Any]:

        try:
            # 用 with 语句管理数据库资源（自动关闭连接/游标，避免泄露）
            with DatabaseConnection() as db:
                query = "SELECT * FROM Location ORDER BY Building, Floor, Room_number"
                with db.connection.cursor(dictionary=True) as cursor:
                    cursor.execute(query)
                    results: List[Dict[str, Any]] = cursor.fetchall()  # 所有位置数据（列表套字典）
                    total_count = len(results)  # 统计位置总数

            # 核心：格式化打印所有位置信息（清晰易读）
            print("=" * 80)
            print(f"📊 所有位置信息（共 {total_count} 条）")
            print("=" * 80)

            if total_count == 0:
                print("❌ 暂无任何位置数据")
            else:
                # 遍历每条位置数据，逐行打印
                for idx, location in enumerate(results, start=1):
                    print(f"\n【位置 {idx}】")
                    print(f"  建筑物：{location.get('Building', '无')}")  # get() 避免字段缺失报错
                    print(f"  楼层：{location.get('Floor', '无')}")
                    print(f"  房号：{location.get('Room_number', '无')}")
                    # 如果表中有其他字段（比如 id、备注），可以在这里补充打印，格式同上

            print("\n" + "=" * 80)  # 打印分隔线，结束输出

            # 返回统一格式的结果（包含总数、数据列表，方便调用者后续使用）
            return {
                "success": True,
                "count": total_count,
                "data": results,
                "message": f"成功查询到 {total_count} 条位置信息"
            }

        except Exception as e:
            # 异常处理：打印错误信息 + 返回失败结果
            error_msg = f"查询所有位置失败：{str(e)}"
            print(f"❌ {error_msg}")
            return {
                "success": False,
                "error": error_msg
            }

    def get_locations_by_building(self, building):
        try:
            ensure_not_empty(building)

            build_valid, build_msg = Validators.validate_building(building)
            if not build_valid:
                return {"success": False, "error": f"Building 验证失败：{build_msg}"}

            db = DatabaseConnection()
            query = "SELECT * FROM Location WHERE Building = %s ORDER BY Floor, Room_number"
            
            cursor = db.connection.cursor(dictionary=True)
            cursor.execute(query, (building,))
            results = cursor.fetchall()
            cursor.close()
            db.close()
            
            return {"success": True, "data": results}
            
        except Exception as e:
            return {"success": False, "error": str(e)}



    def get_vacant_offices(self):
        try:
            db = DatabaseConnection()
            query = "SELECT * FROM Office WHERE OwnerSsn IS NULL ORDER BY Office_Building, Office_Floor, Office_RoomNum"
            
            cursor = db.connection.cursor(dictionary=True)
            cursor.execute(query)
            results = cursor.fetchall()
            cursor.close()
            db.close()
            
            return {"success": True, "data": results}
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    def assign_office_to_employee(self, building: str, floor: int, room_num: int, owner_ssn: str) -> Dict[str, Any]:
        """
        将员工（通过 owner_ssn 标识）分配到指定办公室（building + floor + room_num）
        :param building: 办公室所在建筑物名称
        :param floor: 办公室楼层（非负整数）
        :param room_num: 办公室房号（正整数，>100）
        :param owner_ssn: 员工 SSN（身份证号/工号，非空）
        :return: 统一字典格式结果
        """
        try:
            # 1. 基础非空校验（补充字段名，异常信息更清晰）
            ensure_not_empty(building, "building")
            ensure_not_empty(floor, "floor")
            ensure_not_empty(room_num, "room_num")
            ensure_not_empty(owner_ssn, "owner_ssn")

            # 2. 调用 Validators 做业务规则校验（按字段类型匹配验证函数）
            # 建筑物校验（复用 validate_building：非空 + 长度≤20）
            build_valid, build_msg = Validators.validate_building(building)
            if not build_valid:
                return {"success": False, "error": f"建筑物验证失败：{build_msg}"}

            # 楼层校验（复用 validate_floor：非负整数）
            floor_valid, floor_msg = Validators.validate_floor(floor)
            if not floor_valid:
                return {"success": False, "error": f"楼层验证失败：{floor_msg}"}
            # 补充楼层类型校验（防止传入 float/str 等非整数）
            if not isinstance(floor, int):
                return {"success": False, "error": "楼层必须是整数（不能是小数、字符串等）"}

            # 房号校验（复用 validate_room：正整数 + >100）
            room_valid, room_msg = Validators.validate_room(room_num)
            if not room_valid:
                return {"success": False, "error": f"房号验证失败：{room_msg}"}
            # 补充房号类型校验
            if not isinstance(room_num, int):
                return {"success": False, "error": "房号必须是整数（不能是小数、字符串等）"}

            # 3. SSN 额外校验（非空已做，可根据需求补充长度/格式校验，比如 SSN 是11位数字）
            if not owner_ssn.strip():
                return {"success": False, "error": "员工 SSN 不能是空白字符串"}
            # 可选：如果 SSN 有固定格式（比如11位数字），可添加正则校验
            # import re
            # if not re.match(r'^\d{11}$', owner_ssn):
            #     return {"success": False, "error": "员工 SSN 必须是11位数字"}

            # 4. 验证通过，执行数据库更新（用 with 语句管理资源，避免泄露）
            with DatabaseConnection() as db:
                query = """
                    UPDATE Office 
                    SET OwnerSsn = %s 
                    WHERE Office_Building = %s AND Office_Floor = %s AND Office_RoomNum = %s
                """
                with db.connection.cursor() as cursor:
                    cursor.execute(query, (owner_ssn, building, floor, room_num))
                    db.connection.commit()
                    affected = cursor.rowcount  # 获取受影响的行数（0=未找到办公室，≥1=分配成功）

            # 5. 处理更新结果
            if affected > 0:
                return {
                    "success": True,
                    "message": "办公室分配成功",
                    "data": {
                        "Office_Building": building,
                        "Office_Floor": floor,
                        "Office_RoomNum": room_num,
                        "OwnerSsn": owner_ssn
                    }
                }
            else:
                return {"success": False, "error": "未找到指定办公室（建筑物/楼层/房号不匹配）"}

        except ValueError as ve:
            # 捕获 ensure_not_empty 抛出的空值异常
            return {"success": False, "error": f"参数错误：{str(ve)}"}
        except TypeError as te:
            # 捕获类型错误（比如传入非预期类型）
            return {"success": False, "error": f"参数类型错误：{str(te)}"}
        except Exception as e:
            # 捕获数据库或其他异常
            return {"success": False, "error": f"分配失败：{str(e)}"}

    def vacate_office(self, building: str, floor: int, room_num: int) -> Dict[str, Any]:
        """
        空置指定办公室（将 Office 表中对应记录的 OwnerSsn 设为 NULL）
        :param building: 办公室所在建筑物名称
        :param floor: 办公室楼层（非负整数）
        :param room_num: 办公室房号（正整数，>100）
        :return: 统一字典格式结果：
                 - 成功：{"success": True, "message": "...", "data": {...}}
                 - 失败：{"success": False, "error": "..."}
        """
        try:
            # 1. 基础非空校验（补充字段名，异常信息更清晰）
            ensure_not_empty(building, "building")
            ensure_not_empty(floor, "floor")
            ensure_not_empty(room_num, "room_num")

            # 2. 调用 Validators 做业务规则校验（复用已有验证逻辑，避免重复代码）
            # 建筑物校验：非空 + 长度≤20
            build_valid, build_msg = Validators.validate_building(building)
            if not build_valid:
                return {"success": False, "error": f"建筑物验证失败：{build_msg}"}

            # 楼层校验：非负整数（补充类型校验，防止非整数传入）
            floor_valid, floor_msg = Validators.validate_floor(floor)
            if not floor_valid:
                return {"success": False, "error": f"楼层验证失败：{floor_msg}"}
            if not isinstance(floor, int):
                return {"success": False, "error": "楼层必须是整数（不能是小数、字符串等）"}

            # 房号校验：正整数 + >100（补充类型校验）
            room_valid, room_msg = Validators.validate_room(room_num)
            if not room_valid:
                return {"success": False, "error": f"房号验证失败：{room_msg}"}
            if not isinstance(room_num, int):
                return {"success": False, "error": "房号必须是整数（不能是小数、字符串等）"}

            # 3. 验证通过，执行数据库更新（with 语句自动管理资源，避免泄露）
            with DatabaseConnection() as db:
                query = """
                    UPDATE Office 
                    SET OwnerSsn = NULL 
                    WHERE Office_Building = %s AND Office_Floor = %s AND Office_RoomNum = %s
                """
                with db.connection.cursor() as cursor:
                    cursor.execute(query, (building, floor, room_num))
                    db.connection.commit()
                    affected = cursor.rowcount  # 受影响行数（0=未找到办公室，≥1=空置成功）

            # 4. 处理更新结果（返回统一格式，包含清晰提示）
            if affected > 0:
                return {
                    "success": True,
                    "message": "办公室空置成功（OwnerSsn 已设为 NULL）",
                    "data": {
                        "Office_Building": building,
                        "Office_Floor": floor,
                        "Office_RoomNum": room_num,
                        "OwnerSsn": None  # 明确返回空置后的状态
                    }
                }
            else:
                return {"success": False, "error": "未找到指定办公室（建筑物/楼层/房号不匹配，或该办公室已空置）"}

        except ValueError as ve:
            # 捕获空值异常（ensure_not_empty 抛出）
            return {"success": False, "error": f"参数错误：{str(ve)}"}
        except TypeError as te:
            # 捕获类型错误（比如传入非预期类型）
            return {"success": False, "error": f"参数类型错误：{str(te)}"}
        except Exception as e:
            # 捕获数据库或其他未预期异常
            return {"success": False, "error": f"办公室空置失败：{str(e)}"}