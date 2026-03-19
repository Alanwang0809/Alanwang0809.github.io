#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
手动创建简单的.docx文件
.docx文件本质上是ZIP压缩的XML文件
"""

import zipfile
import os
import datetime

def create_simple_docx(filename):
    """创建最简单的.docx文件"""
    
    # 基本的.docx文件结构
    docx_structure = {
        '[Content_Types].xml': '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
    <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
    <Default Extension="xml" ContentType="application/xml"/>
    <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
    <Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
</Types>''',
        
        '_rels/.rels': '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
    <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>''',
        
        'word/_rels/document.xml.rels': '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
    <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
</Relationships>''',
        
        'word/document.xml': '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
    <w:body>
        <w:p>
            <w:r>
                <w:t>测试Word文件：1.docx</w:t>
            </w:r>
        </w:p>
        <w:p>
            <w:r>
                <w:t>创建时间：''' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '''</w:t>
            </w:r>
        </w:p>
        <w:p>
            <w:r>
                <w:t>创建者：小龙虾 🦞</w:t>
            </w:r>
        </w:p>
        <w:p>
            <w:r>
                <w:t>测试目的：验证手动创建Word文件的能力</w:t>
            </w:r>
        </w:p>
        <w:p>
            <w:r>
                <w:t>这是通过手动创建XML结构生成的.docx文件</w:t>
            </w:r>
        </w:p>
        <w:p>
            <w:r>
                <w:t>虽然内容简单，但确实是有效的Word文档</w:t>
            </w:r>
        </w:p>
        <w:sectPr>
            <w:pgSz w:w="11906" w:h="16838"/>
            <w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440" w:header="851" w:footer="992" w:gutter="0"/>
            <w:cols w:space="720"/>
            <w:docGrid w:linePitch="360"/>
        </w:sectPr>
    </w:body>
</w:document>''',
        
        'word/styles.xml': '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
    <w:style w:type="paragraph" w:default="1" w:styleId="Normal">
        <w:name w:val="Normal"/>
        <w:qFormat/>
    </w:style>
</w:styles>'''
    }
    
    try:
        # 创建ZIP文件（.docx本质上是ZIP）
        with zipfile.ZipFile(filename, 'w', zipfile.ZIP_DEFLATED) as docx_zip:
            for file_path, content in docx_structure.items():
                docx_zip.writestr(file_path, content)
        
        print(f"✅ 成功创建Word文件: {filename}")
        print(f"文件大小: {os.path.getsize(filename)} 字节")
        return True
        
    except Exception as e:
        print(f"❌ 创建Word文件失败: {e}")
        return False

def main():
    """主函数"""
    print("开始手动创建Word文件...")
    
    # 尝试保存到桌面
    desktop_path = "C:\\Users\\sbjpk\\Desktop\\1.docx"
    
    # 先尝试保存到工作空间
    workspace_path = "test_files/1.docx"
    
    print(f"尝试保存到: {workspace_path}")
    
    if create_simple_docx(workspace_path):
        print("\n✅ Word文件创建成功！")
        print(f"文件位置: {workspace_path}")
        
        # 尝试复制到桌面
        try:
            import shutil
            shutil.copy2(workspace_path, desktop_path)
            print(f"✅ 已复制到桌面: {desktop_path}")
        except Exception as e:
            print(f"⚠️ 无法复制到桌面: {e}")
            print("文件保存在工作空间，可以通过飞书发送")
            
        return workspace_path
    else:
        print("\n❌ Word文件创建失败")
        return None

if __name__ == "__main__":
    main()