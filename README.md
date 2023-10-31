# PDF文本替换工具

这是一个基于Python的工具，用于替换PDF文件中的文本。该工具接受一个输入PDF文件、一个输出PDF文件和一个包含替换规则的JSON字符串。

## 安装

首先，确保你已经安装了Python（3.x版本）。

然后，安装依赖包。

```bash
pip install PyMuPDF argparse
```

或者从`requirements.txt`文件中安装（如果有）。

```bash
pip install -r requirements.txt
```

## 使用方法

通过命令行参数来运行该脚本。参数说明如下：

- `--ipdf`：指定输入PDF文件的路径（必须）。
- `--opdf`：指定输出PDF文件的路径，也就是保存修改后的PDF文件（必须）。
- `--replace`：指定一个JSON字符串，用于定义需要替换的文本以及对应的替换内容（必须）。

### 示例

下面是一个命令行使用示例：

```bash
python script.py --ipdf input.pdf --opdf output.pdf --replace "{\"old_text\": \"new_text\"}"
```

或者，如果你有多组文本需要替换：

```bash
python script.py --ipdf input.pdf --opdf output.pdf --replace "{\"old_text1\": \"new_text1\", \"old_text2\": \"new_text2\"}"
```

### 替换规则JSON字符串

该字符串必须是一个有效的JSON对象，其中的键是需要替换的原文本，值是用于替换的新文本。

示例：

```json
{
    "N.D.N.": "ASL",
    "B.V.B.A.": "Liege"
}
```

需要转换成单行，并确保键和值都用双引号括起来。例如：

```bash
"{\"N.D.N.\": \"ASL\", \"B.V.B.A.\": \"Liege\"}"
```

这样的字符串可以直接用作`--replace`参数的值。

## 注意事项

- 请确保你有权修改和处理目标PDF文件。
- 替换文本的字体大小和类型可以在源代码中进行调整。

## 开发者

- [你的名字或组织]

## 许可

[适当的开源许可]

希望这个README.md文件对您有所帮助！如果你有其他问题或需要进一步的澄清，请随时提出。

