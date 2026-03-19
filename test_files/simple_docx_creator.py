#!/usr/bin/env python
"""
创建最简单的.docx文件
使用最基础的方法
"""

import zipfile
import os

# 创建一个最简单的.docx文件结构
# .docx文件本质上是包含特定XML文件的ZIP压缩包

def create_minimal_docx(filename):
    """创建最小化的.docx文件"""
    
    # 最基本的.docx文件内容
    files = {
        '[Content_Types].xml': '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
<Default Extension="xml" ContentType="application/xml"/>
<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
</Types>''',
        
        '_rels/.rels': '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>''',
        
        'word/_rels/document.xml.rels': '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
</Relationships>''',
        
        'word/document.xml': '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
<w:body>
<w:p><w:r><w:t>测试文件：1.docx</w:t></w:r></w:p>
<w:p><w:r><w:t>创建时间：2026-03-16</w:t></w:r></w:p>
<w:p><w:r><w:t>创建者：小龙虾</w:t></w:r></w:p>
<w:p><w:r><w:t>这是一个最简单的Word文档测试文件。</w:t></w:r></w:p>
<w:p><w:r><w:t>虽然简单，但是有效的.docx格式。</w:t></w:r></w:p>
</w:body>
</w:document>'''
    }
    
    try:
        # 创建ZIP文件
        with zipfile.ZipFile(filename, 'w') as zf:
            for name, content in files.items():
                zf.writestr(name, content)
        
        print(f"创建成功: {filename}")
        print(f"文件大小: {os.path.getsize(filename)} 字节")
        return True
        
    except Exception as e:
        print(f"创建失败: {e}")
        return False

if __name__ == "__main__":
    # 尝试在工作空间创建
    output_file = "test_files/1.docx"
    
    print("尝试创建最简单的.docx文件...")
    if create_minimal_docx(output_file):
        print("✅ 文件创建成功！")
        print(f"文件位置: {output_file}")
    else:
        print("❌ 文件创建失败")