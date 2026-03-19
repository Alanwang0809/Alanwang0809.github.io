// 将Markdown文件转换为Word文档
const { Document, Packer, Paragraph, TextRun, HeadingLevel } = require("docx");
const fs = require("fs");
const path = require("path");

console.log("开始将Markdown转换为Word文档...");

// 读取Markdown文件
function readMarkdownFile(filePath) {
    try {
        const content = fs.readFileSync(filePath, 'utf-8');
        console.log(`✅ 成功读取文件: ${path.basename(filePath)}`);
        console.log(`文件大小: ${content.length} 字符`);
        return content;
    } catch (error) {
        console.error(`❌ 读取文件失败: ${error.message}`);
        return null;
    }
}

// 简单的Markdown解析（基础功能）
function parseMarkdownToDocx(markdownContent) {
    const lines = markdownContent.split('\n');
    const paragraphs = [];
    
    for (let line of lines) {
        line = line.trim();
        
        if (line.length === 0) {
            // 空行
            paragraphs.push(new Paragraph({}));
            continue;
        }
        
        // 检查标题
        if (line.startsWith('# ')) {
            // 一级标题
            paragraphs.push(new Paragraph({
                text: line.substring(2),
                heading: HeadingLevel.HEADING_1,
            }));
        } else if (line.startsWith('## ')) {
            // 二级标题
            paragraphs.push(new Paragraph({
                text: line.substring(3),
                heading: HeadingLevel.HEADING_2,
            }));
        } else if (line.startsWith('### ')) {
            // 三级标题
            paragraphs.push(new Paragraph({
                text: line.substring(4),
                heading: HeadingLevel.HEADING_3,
            }));
        } else if (line.startsWith('- ') || line.startsWith('* ')) {
            // 列表项
            paragraphs.push(new Paragraph({
                text: `• ${line.substring(2)}`,
                bullet: { level: 0 },
            }));
        } else if (line.startsWith('**') && line.endsWith('**')) {
            // 粗体文本
            paragraphs.push(new Paragraph({
                children: [
                    new TextRun({
                        text: line.substring(2, line.length - 2),
                        bold: true,
                    }),
                ],
            }));
        } else {
            // 普通段落
            paragraphs.push(new Paragraph({
                text: line,
            }));
        }
    }
    
    return paragraphs;
}

// 转换单个文件
function convertMarkdownToDocx(mdFilePath, docxFilePath) {
    console.log(`\n开始转换: ${path.basename(mdFilePath)}`);
    
    // 读取Markdown文件
    const markdownContent = readMarkdownFile(mdFilePath);
    if (!markdownContent) {
        return false;
    }
    
    // 解析Markdown
    const paragraphs = parseMarkdownToDocx(markdownContent);
    
    // 创建Word文档
    const doc = new Document({
        sections: [{
            properties: {},
            children: [
                // 添加转换说明
                new Paragraph({
                    children: [
                        new TextRun({
                            text: "📄 文件格式转换说明",
                            bold: true,
                            size: 32,
                        }),
                    ],
                }),
                new Paragraph({
                    text: `原始文件: ${path.basename(mdFilePath)}`,
                }),
                new Paragraph({
                    text: `转换时间: ${new Date().toLocaleString('zh-CN')}`,
                }),
                new Paragraph({
                    text: `转换工具: Node.js docx库`,
                }),
                new Paragraph({
                    text: "说明: 此文件由Markdown格式转换为Word格式，部分复杂格式可能简化",
                }),
                new Paragraph({}),
                new Paragraph({
                    children: [
                        new TextRun({
                            text: "--- 以下是原始文件内容 ---",
                            bold: true,
                        }),
                    ],
                }),
                new Paragraph({}),
                
                // 添加原始内容
                ...paragraphs,
            ],
        }],
    });
    
    // 保存Word文档
    return Packer.toBuffer(doc)
        .then((buffer) => {
            fs.writeFileSync(docxFilePath, buffer);
            const fileSize = fs.statSync(docxFilePath).size;
            
            console.log(`✅ 转换成功: ${path.basename(docxFilePath)}`);
            console.log(`文件大小: ${fileSize} 字节`);
            console.log(`保存位置: ${docxFilePath}`);
            
            return true;
        })
        .catch((error) => {
            console.error(`❌ 转换失败: ${error.message}`);
            return false;
        });
}

// 主函数
async function main() {
    console.log("Markdown转Word转换器启动...");
    
    // 定义要转换的文件
    const filesToConvert = [
        {
            mdPath: "C:\\Users\\sbjpk\\Desktop\\行业研究\\1_AI人工智能\\AI产业链深度研究报告_2026-03-15.md",
            docxName: "AI产业链深度研究报告_2026-03-15.docx"
        },
        {
            mdPath: "C:\\Users\\sbjpk\\Desktop\\行业研究\\1_AI人工智能\\AI产业链研究摘要_2026-03-15.md",
            docxName: "AI产业链研究摘要_2026-03-15.docx"
        },
        {
            mdPath: "C:\\Users\\sbjpk\\Desktop\\行业研究\\1_AI人工智能\\AI行业研究模板.md",
            docxName: "AI行业研究模板.docx"
        }
    ];
    
    const results = [];
    
    // 转换每个文件
    for (const file of filesToConvert) {
        const docxPath = path.join(__dirname, file.docxName);
        
        try {
            const success = await convertMarkdownToDocx(file.mdPath, docxPath);
            results.push({
                name: file.docxName,
                success: success,
                path: docxPath
            });
            
            // 短暂延迟，避免过快
            await new Promise(resolve => setTimeout(resolve, 500));
            
        } catch (error) {
            console.error(`转换 ${file.docxName} 时出错: ${error.message}`);
            results.push({
                name: file.docxName,
                success: false,
                error: error.message
            });
        }
    }
    
    // 输出结果
    console.log("\n" + "=".repeat(50));
    console.log("转换结果汇总:");
    console.log("=".repeat(50));
    
    let successCount = 0;
    for (const result of results) {
        if (result.success) {
            console.log(`✅ ${result.name}: 成功`);
            successCount++;
        } else {
            console.log(`❌ ${result.name}: 失败 - ${result.error || '未知错误'}`);
        }
    }
    
    console.log("=".repeat(50));
    console.log(`总计: ${successCount}/${results.length} 个文件转换成功`);
    
    return results;
}

// 执行转换
if (require.main === module) {
    main().then(results => {
        if (results.some(r => r.success)) {
            console.log("\n✅ 转换完成！可以发送Word文件了。");
            process.exit(0);
        } else {
            console.log("\n❌ 所有文件转换失败");
            process.exit(1);
        }
    }).catch(error => {
        console.error(`主程序错误: ${error.message}`);
        process.exit(1);
    });
}

module.exports = { convertMarkdownToDocx };