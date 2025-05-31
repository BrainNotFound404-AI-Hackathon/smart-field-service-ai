# 导入必要的库
import random
from datetime import datetime, timedelta
import json
import argparse

def generate_elevator_data(num_entries=1000, fault_ratio=0.1):
    """
    生成模拟电梯运行数据的列表。
    参数:
        num_entries (int): 生成的数据条数。
        fault_ratio (float): 注入故障的数据比例 (0~1之间)。
    返回:
        list: 包含模拟数据条目的列表，每个条目为一个字典，结构与指定 JSON 格式一致。
    """
    data = []
    # 计算需要插入故障的条目数量 (向下取整)
    num_faults = int(num_entries * fault_ratio)
    # 随机选择哪些索引的条目注入故障
    fault_indices = set(random.sample(range(num_entries), num_faults))
    
    # 时间范围：当前时间前后各7天 (使用 UTC 时间)
    now = datetime.utcnow()
    start_time = now - timedelta(days=7)
    end_time = now + timedelta(days=7)
    total_duration = end_time - start_time
    
    # 如果只需生成1条数据，直接返回当前时间点的数据
    if num_entries <= 1:
        ts = start_time + total_duration * 0.5  # 时间点选在中间，即当前时间
        timestamp = ts.strftime("%Y-%m-%dT%H:%M:%SZ")  # ISO8601格式时间戳
        entry = {
            "timestamp": timestamp,
            "status": "idle",
            "environment": {
                "temperature_c": 25.0,
                "humidity_percent": 50.0
            },
            "sensors": {
                "vibration_rms": 0.0,
                "motor_current_a": 0.0,
                "car_load_kg": 0.0,
                "acceleration_m_s2": 0.0
            },
            "fault_codes": []
        }
        return [entry]
    
    # 计算连续时间范围内每条数据的时间步长 (秒)
    total_seconds = total_duration.total_seconds()
    step = total_seconds / (num_entries - 1)
    
    for i in range(num_entries):
        # 生成该条数据的时间戳 (在开始时间基础上偏移 i*step 秒)
        ts = start_time + timedelta(seconds=i * step)
        timestamp = ts.strftime("%Y-%m-%dT%H:%M:%SZ")  # 格式化时间戳为字符串
        
        # 随机确定电梯状态: 50% 概率空闲, 25% 上行, 25% 下行
        if random.random() < 0.5:
            status = "idle"
        else:
            status = random.choice(["moving_up", "moving_down"])
        
        # 环境传感器数据：温度和湿度在正常范围内随机波动
        temperature = random.uniform(18.0, 28.0)      # 温度 (°C)，一般在18~28°C之间
        humidity = random.uniform(30.0, 70.0)         # 湿度 (%)，一般在30%~70%之间
        
        # 电梯载荷 (轿厢载重): 大部分时间载荷较低，偶尔接近满载
        if random.random() < 0.5:
            car_load = random.uniform(0, 200)         # 约50%时间0~200kg，模拟空载或少量乘客
        elif random.random() < 0.8:
            car_load = random.uniform(200, 600)       # 约30%时间200~600kg，中等载荷
        else:
            car_load = random.uniform(600, 1000)      # 约20%时间600~1000kg，接近满载
        
        # 电机电流 (A): 根据状态和载荷确定基本值
        if status == "idle":
            # 空闲状态，电机电流接近0，仅维持待机和门机等少量电流
            motor_current = random.uniform(0, 5)
        else:
            # 运行状态，基准电流和载荷相关
            base_current = random.uniform(10, 30)     # 电梯空载运行的基准电流
            load_factor = 0.05                        # 电流随载荷增加的系数 (假设值)
            motor_current = base_current + load_factor * car_load
            if status == "moving_down":
                # 下行时由于重力平衡，电机电流相对更小 (可能出现再生制动)，这里用0.5~0.8倍模拟
                motor_current *= random.uniform(0.5, 0.8)
        
        # 振动 RMS: 空闲时振动很小，运行时有一定振动
        if status == "idle":
            vibration = random.uniform(0.0, 0.2)
        else:
            vibration = random.uniform(0.5, 1.5)
        
        # 加速度 (m/s^2): 平稳运行或静止时接近0，只有加减速时才有较大值
        if status == "idle":
            accel = 0.0
        else:
            # 假设仅有10%的运行时刻处于加速或减速阶段，其余为匀速 (加速度≈0)
            if random.random() < 0.1:
                accel = random.uniform(-1.0, 1.0)     # 小幅加速度或减速度
            else:
                accel = 0.0
        
        fault_codes = []
        
        # 检查该条目是否需要注入故障
        if i in fault_indices:
            # 简化为3个基本故障代码
            # 101: 门系统故障
            # 201: 驱动系统故障
            # 301: 安全系统故障
            faults = [101, 201, 301]
            fault_code = random.choice(faults)
            fault_codes = [fault_code]
            
            # 根据故障代码调整相关指标以模拟故障发生
            if fault_code == 101:
                # 故障101: 门系统故障
                status = "idle"
                # 门机电流增大
                motor_current += random.uniform(10, 20)
                # 门反复尝试开启/关闭可能引起振动增加
                vibration += random.uniform(0.5, 1.0)
                # 电梯未运动，加速度为0
                accel = 0.0
            elif fault_code == 201:
                # 故障201: 驱动系统故障
                if status == "idle":
                    status = random.choice(["moving_up", "moving_down"])
                # 电机电流异常升高
                motor_current += random.uniform(30, 50)
                # 振动增大
                vibration += random.uniform(0.5, 1.5)
                # 加速度波动
                accel += random.uniform(-0.5, 0.5)
            elif fault_code == 301:
                # 故障301: 安全系统故障
                status = "idle"
                # 超载保护触发
                car_load = max(car_load, random.uniform(1000, 1300))
                # 电机电流激增后触发保护
                motor_current += random.uniform(20, 40)
                # 振动增加
                vibration += random.uniform(0.5, 1.5)
                # 电梯停止，加速度为0
                accel = 0.0
            
            # 边界修正
            if motor_current < 0:
                motor_current = 0.0
            if accel > 15:
                accel = 15.0
            if accel < -15:
                accel = -15.0
        
        # 将数值保留适当的小数位，提高结果可读性
        entry = {
            "timestamp": timestamp,
            "status": status,
            "environment": {
                "temperature_c": round(temperature, 2),
                "humidity_percent": round(humidity, 2)
            },
            "sensors": {
                "vibration_rms": round(vibration, 3),
                "motor_current_a": round(motor_current, 2),
                "car_load_kg": round(car_load, 1),
                "acceleration_m_s2": round(accel, 3)
            },
            "fault_codes": fault_codes
        }
        data.append(entry)
    return data

if __name__ == "__main__":
    # 命令行参数解析，用于自定义数据量、故障比例和输出格式/文件
    parser = argparse.ArgumentParser(description="模拟生成电梯运行状态数据，并支持导出为 JSON 或 JSONL 格式文件。")
    parser.add_argument("-n", "--num_entries", type=int, default=1000,
                        help="生成的数据条数 (默认: 1000)")
    parser.add_argument("-f", "--fault_ratio", type=float, default=0.1,
                        help="故障数据比例 (默认: 0.1 表示 10%)")
    parser.add_argument("--format", choices=["json", "jsonl"], default="json",
                        help="输出格式: 'json' 输出 JSON 数组, 'jsonl' 输出 JSON Lines 逐行记录 (默认: json)")
    parser.add_argument("-o", "--output", type=str, default=None,
                        help="输出文件路径，如未指定则打印至标准输出")
    args = parser.parse_args()
    
    # 生成数据
    data = generate_elevator_data(num_entries=args.num_entries, fault_ratio=args.fault_ratio)
    
    # 根据指定格式输出数据
    if args.output:
        # 将数据写入文件
        if args.format == "json":
            # JSON 数组格式输出
            with open(args.output, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
        else:
            # JSONL 格式，每条记录单独一行
            with open(args.output, 'w', encoding='utf-8') as f:
                for entry in data:
                    json_line = json.dumps(entry, ensure_ascii=False)
                    f.write(json_line + "\n")
        print(f"数据已成功写入 {args.output} ({args.format.upper()} 格式)。")
    else:
        # 未指定输出文件，打印到标准输出
        if args.format == "json":
            print(json.dumps(data, ensure_ascii=False, indent=2))
        else:
            for entry in data:
                print(json.dumps(entry, ensure_ascii=False))