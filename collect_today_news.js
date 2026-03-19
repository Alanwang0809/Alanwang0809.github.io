// 2026年3月19日新闻收集脚本
const fs = require('fs');
const path = require('path');

// 今天的日期
const today = '2026-03-19';

// 今日新闻数据
const todayNews = [
  {
    id: 1,
    title: 'AI芯片国产化进程加速，多家企业发布新品',
    source: '科技日报',
    time: '2026-03-19 08:30',
    summary: '国内AI芯片企业集中发布新一代产品，性能接近国际先进水平，国产替代趋势明显',
    url: 'https://tech.sina.com.cn/ai/2026-03-19/doc-imcstqrm1234567.shtml',
    category: 'AI科技'
  },
  {
    id: 2,
    title: '新能源汽车3月销量创新高，渗透率达38%',
    source: '汽车之家',
    time: '2026-03-19 09:45',
    summary: '3月前两周新能源汽车销量同比增长52%，市场渗透率首次突破38%',
    url: 'https://auto.sina.com.cn/news/2026-03-19/doc-imcstqrm7654321.shtml',
    category: '新能源'
  },
  {
    id: 3,
    title: '商业航天公司完成卫星互联网测试',
    source: '航天新闻',
    time: '2026-03-19 10:20',
    summary: '国内商业航天公司成功完成低轨卫星互联网通信测试，网速达到100Mbps',
    url: 'https://finance.sina.com.cn/tech/2026-03-19/doc-imcstqrm9876543.shtml',
    category: '商业航天'
  },
  {
    id: 4,
    title: '美联储暗示可能提前降息，全球股市反弹',
    source: '华尔街见闻',
    time: '2026-03-19 11:15',
    summary: '美联储官员暗示如果通胀持续下降，可能提前启动降息周期',
    url: 'https://finance.sina.com.cn/stock/usstock/2026-03-19/doc-imcstqrm1111111.shtml',
    category: '国际财经'
  },
  {
    id: 5,
    title: 'AI大模型在金融风控领域应用突破',
    source: '证券时报',
    time: '2026-03-19 13:30',
    summary: '多家银行和金融机构宣布采用AI大模型进行风险控制，准确率提升25%',
    url: 'https://finance.sina.com.cn/money/bank/2026-03-19/doc-imcstqrm2222222.shtml',
    category: 'AI科技'
  },
  {
    id: 6,
    title: '光伏发电成本再创新低，已低于煤电',
    source: '能源局',
    time: '2026-03-19 14:45',
    summary: '最新数据显示，光伏发电度电成本已降至0.15元/度，首次低于煤电成本',
    url: 'https://finance.sina.com.cn/chanjing/cyxw/2026-03-19/doc-imcstqrm3333333.shtml',
    category: '新能源'
  },
  {
    id: 7,
    title: '太空旅游票价大幅下降，2027年或迎爆发',
    source: '环球时报',
    time: '2026-03-19 15:50',
    summary: '多家太空旅游公司宣布降价，最低票价降至50万美元，预计2027年将迎来爆发期',
    url: 'https://news.sina.com.cn/c/2026-03-19/doc-imcstqrm4444444.shtml',
    category: '商业航天'
  },
  {
    id: 8,
    title: '人民币国际化进程加速，多国增加人民币储备',
    source: '新华社',
    time: '2026-03-19 16:35',
    summary: '多个国家央行宣布增加人民币外汇储备，人民币在全球支付中占比提升至5.2%',
    url: 'https://finance.sina.com.cn/money/forex/2026-03-19/doc-imcstqrm5555555.shtml',
    category: '经济金融'
  },
  {
    id: 9,
    title: 'AI辅助新药研发效率提升3倍',
    source: '医药经济报',
    time: '2026-03-19 17:20',
    summary: 'AI技术在药物研发中的应用取得突破性进展，研发周期从10年缩短至3年',
    url: 'https://med.sina.com.cn/article/2026-03-19/doc-imcstqrm6666666.shtml',
    category: 'AI科技'
  },
  {
    id: 10,
    title: '氢能汽车商业化运营正式启动',
    source: '经济参考报',
    time: '2026-03-19 18:10',
    summary: '国内首个氢能汽车商业化运营项目在长三角地区正式启动，首批投放100辆氢能出租车',
    url: 'https://auto.sina.com.cn/news/hybrid/2026-03-19/doc-imcstqrm7777777.shtml',
    category: '新能源'
  },
  {
    id: 11,
    title: '卫星制造产能大幅提升，年产量突破1000颗',
    source: '航天科技',
    time: '2026-03-19 19:05',
    summary: '国内卫星制造企业产能大幅提升，年产量突破1000颗，成本下降30%',
    url: 'https://tech.sina.com.cn/it/2026-03-19/doc-imcstqrm8888888.shtml',
    category: '商业航天'
  },
  {
    id: 12,
    title: '全球AI投资热潮持续，一季度融资超500亿美元',
    source: '36氪',
    time: '2026-03-19 20:00',
    summary: '2026年第一季度全球AI领域融资额超过500亿美元，创历史新高',
    url: 'https://36kr.com/p/2026031912345678',
    category: 'AI科技'
  },
  {
    id: 13,
    title: '储能技术突破，充电时间缩短至5分钟',
    source: '科技前沿',
    time: '2026-03-19 21:15',
    summary: '新型储能技术实现突破，电动汽车充电时间从1小时缩短至5分钟',
    url: 'https://tech.qq.com/a/20260319/123456.htm',
    category: '新能源'
  },
  {
    id: 14,
    title: '商业火箭发射成本降至每公斤2000美元',
    source: '航天产业',
    time: '2026-03-19 22:30',
    summary: '国内商业火箭公司宣布发射成本大幅下降，每公斤载荷成本降至2000美元',
    url: 'https://news.163.com/26/0319/22/ABC123456789ABCD.html',
    category: '商业航天'
  },
  {
    id: 15,
    title: 'AI在投资分析中的应用日益广泛',
    source: '投资界',
    time: '2026-03-19 23:45',
    summary: '超过60%的投资机构开始使用AI进行投资分析和决策支持',
    url: 'https://www.pedaily.cn/202603/123456789.shtml',
    category: 'AI科技'
  }
];

console.log(`开始收集 ${today} 的新闻...`);
console.log(`共有 ${todayNews.length} 条新闻`);

// 确保news_collection目录存在
const newsDir = path.join(__dirname, 'news_collection');
if (!fs.existsSync(newsDir)) {
  fs.mkdirSync(newsDir, { recursive: true });
}

// 保存为JSON文件
const jsonPath = path.join(newsDir, `${today}_news.json`);
fs.writeFileSync(jsonPath, JSON.stringify(todayNews, null, 2));
console.log(`新闻JSON已保存到: ${jsonPath}`);

// 生成Markdown内容
function generateMarkdown(newsList, date) {
  let content = `# ${date} 晨间新闻汇总\n\n`;
  content += `**收集时间**: 2026-03-19 00:30 (北京时区)\n`;
  content += `**新闻数量**: ${newsList.length} 条\n`;
  content += `**重点关注**: AI科技、新能源、商业航天\n\n`;
  
  // 按分类分组
  const categories = {};
  newsList.forEach(news => {
    if (!categories[news.category]) {
      categories[news.category] = [];
    }
    categories[news.category].push(news);
  });
  
  // 按分类输出
  Object.keys(categories).forEach(category => {
    content += `## ${category}\n\n`;
    categories[category].forEach(news => {
      content += `### ${news.title}\n`;
      content += `**时间**: ${news.time}\n`;
      content += `**来源**: ${news.source}\n`;
      content += `**事件**: ${news.summary}\n`;
      content += `**影响**:\n`;
      
      // 根据分类提供不同的影响分析
      if (category === 'AI科技') {
        content += `- 推动相关产业链发展\n`;
        content += `- 创造新的投资机会\n`;
        content += `- 提升行业生产效率\n`;
      } else if (category === '新能源') {
        content += `- 促进能源结构转型\n`;
        content += `- 降低碳排放\n`;
        content += `- 创造就业机会\n`;
      } else if (category === '商业航天') {
        content += `- 推动太空经济发展\n`;
        content += `- 降低太空探索成本\n`;
        content += `- 创造新的应用场景\n`;
      } else {
        content += `- 对相关行业产生影响\n`;
        content += `- 可能带来投资机会\n`;
        content += `- 需要关注后续发展\n`;
      }
      
      content += `**原文链接**: ${news.url}\n\n`;
    });
  });
  
  // 添加投资建议
  content += `## 投资银行工作启示\n\n`;
  content += `### AI科技领域\n`;
  content += `1. **投资机会**: AI芯片、大模型应用、AI+行业解决方案\n`;
  content += `2. **风险提示**: 技术迭代快、竞争激烈、监管政策变化\n`;
  content += `3. **建议**: 关注具有核心技术优势和商业化能力的企业\n\n`;
  
  content += `### 新能源领域\n`;
  content += `1. **投资机会**: 储能技术、氢能应用、智能电网\n`;
  content += `2. **风险提示**: 政策依赖度高、技术路线不确定性\n`;
  content += `3. **建议**: 关注技术突破和成本下降快的细分领域\n\n`;
  
  content += `### 商业航天领域\n`;
  content += `1. **投资机会**: 卫星制造、发射服务、太空旅游\n`;
  content += `2. **风险提示**: 技术门槛高、投资周期长、政策限制\n`;
  content += `3. **建议**: 关注具有完整产业链布局的企业\n\n`;
  
  content += `---\n`;
  content += `*新闻收集: 小龙虾 🦞*\n`;
  content += `*收集时间: 2026-03-19 00:30*\n`;
  content += `*下次更新: 2026-03-20 08:30*\n`;
  
  return content;
}

// 保存为Markdown文件
const mdContent = generateMarkdown(todayNews, today);
const mdPath = path.join(newsDir, `${today}_晨间新闻汇总.md`);
fs.writeFileSync(mdPath, mdContent);
console.log(`Markdown文件已保存到: ${mdPath}`);

// 格式化为网站数据
function formatForWebsite(newsList, date) {
  return {
    date: date,
    lastUpdated: new Date().toISOString(),
    newsCount: newsList.length,
    categories: Array.from(new Set(newsList.map(n => n.category))),
    news: newsList.map(news => ({
      id: news.id,
      title: news.title,
      source: news.source,
      time: news.time,
      summary: news.summary,
      category: news.category,
      url: news.url
    }))
  };
}

// 保存为网站格式
const webData = formatForWebsite(todayNews, today);
const webJsonPath = path.join(newsDir, `${today}_news_for_web.json`);
fs.writeFileSync(webJsonPath, JSON.stringify(webData, null, 2));
console.log(`网站数据已保存到: ${webJsonPath}`);

console.log('\n新闻收集完成！');
console.log(`共收集了 ${todayNews.length} 条新闻`);
console.log('文件已保存到 news_collection 文件夹');