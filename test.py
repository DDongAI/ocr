import csv
import json
def main(csv_string):
    # 将csv字符串分割成行
    lines = csv_string.strip().split('\n')

    # 创建一个CSV读取器
    reader = csv.reader(lines)

    # 将所有行转换为列表
    data = [row for row in reader]

    # 将数字列转换为浮点数
    for row in data[1:]:  # 跳过表头行
        for i in range(1, len(row)):
            try:
                row[i] = float(row[i])
            except ValueError:
                pass

    echarts_config = {
        "lengend": {},
        "tootip": {},
        "dataset": {
            "source": data
        },
        "xAxis": [
            {
                "type": "category",
                "gridIndex": 0,
            },
            {
                "type": "category",
                "gridIndex": 1,
            }
        ],
        "yAxis": [
            {
                "gridIndex": 0,
            },
            {
                "gridIndex": 1,
            }
        ],
        "gird": [
            {"bottom": "55%"},
            {"top": "55%"}
        ],
        "series": [
            # 折线图
            {"type": "bar", "seriesLayoutBy": "row"},
            {"type": "bar", "seriesLayoutBy": "row"},
            {"type": "bar", "seriesLayoutBy": "row"},
            {"type": "bar", "seriesLayoutBy": "row"},

            # 柱状图
            {"type": "bar", "xAxisIndex": 1, "yAxisIndex": 1},
            {"type": "bar", "xAxisIndex": 1, "yAxisIndex": 1},
            {"type": "bar", "xAxisIndex": 1, "yAxisIndex": 1},
            {"type": "bar", "xAxisIndex": 1, "yAxisIndex": 1},
            {"type": "bar", "xAxisIndex": 1, "yAxisIndex": 1},
            {"type": "bar", "xAxisIndex": 1, "yAxisIndex": 1},
            {"type": "bar", "xAxisIndex": 1, "yAxisIndex": 1},

        ]
    }

    ouput = f'```eCharts\n{json.dumps(echarts_config,ensure_ascii=False, indent=4)}\n```'

    return {"result": ouput}



