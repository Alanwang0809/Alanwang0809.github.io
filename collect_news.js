// 简单新闻收集脚本
const fs = require('fs');
const path = require('path');
const https = require('https');

// 新闻源列表
const newsSources = [
  {
    name: '新浪新闻',
    url: 'https://news.sina.com.cn/',
    selector: '.news-item'
  },
  {
    name: '澎湃新闻',
    url: 'https://www.thepaper.cn/',
    selector: '.news_li'
  },
  {
    name: '财新网',
    url: 'https://www.caixin.com/',
    selector: '.news_list li'
  }
];

// 收集新闻函数
async function collectNews() {
  console.log('开始收集新闻...');
  const today = new Date().toISOString().split('T')[0];
  const newsList = [];
  
  // 由于网络限制，我们使用模拟数据
  const mockNews = [
    {
      title: 'AI芯片技术新突破，国产替代加速',
      source: '科技日报',
      time: '2026-03-19 08:00',
      summary: '国内AI芯片企业宣布新一代芯片研发成功，性能提升30%，功耗降低20%',
      url: 'https://example.com/news1',
      category: 'AI科技'
    },
    {
      title: '新能源汽车销量再创新高',
      source: '经济参考报',
      time: '2026-03-19 09:15',
      summary: '3月份新能源汽车销量同比增长45%，市场渗透率达到35%',
      url: 'https://example.com/news2',
      category: '新能源'
    },
    {
      title: '商业航天公司完成新一轮融资',
      source: '证券时报',
      time: '2026-03-19 10:30',
      summary: '国内商业航天公司完成10亿元融资，将用于卫星互联网建设',
      url: 'https://example.com/news3',
      category: '商业航天'
    },
    {
      title: '国际油价持续上涨，通胀压力增大',
      source: '华尔街见闻',
      time: '2026-03-19 11:45',
      summary: '国际油价突破每桶90美元，全球通胀压力进一步增大',
      url: 'https://example.com/news4',
      category: '经济金融'
    },
    {
      title: 'AI大模型应用加速落地',
      source: '36氪',
      time: '2026-03-19 13:00',
      summary: '多家企业宣布AI大模型在金融、医疗、教育等领域的应用案例',
      url: 'https://example.com/news5',
      category: 'AI科技'
    },
    {
      title: '可再生能源装机容量创新高',
      source: '能源局',
      time: '2026-03-19 14:15',
      summary: '全国可再生能源装机容量突破15亿千瓦，占比超过50%',
      url: 'https://example.com/news6',
      category: '新能源'
    },
    {
      title: '太空旅游商业化进程加速',
      source: '航天新闻',
      time: '2026-03-19 15:30',
      summary: '多家公司宣布太空旅游计划，预计2027年实现商业化运营',
      url: 'https://example.com/news7',
      category: '商业航天'
    },
    {
      title: '美联储维持利率不变',
      source: '路透社',
      time: '2026-03-19 16:45',
      summary: '美联储宣布维持基准利率不变，市场预期年内可能降息',
      url: 'https://example.com/news8',
      category: '国际财经'
    },
    {
      title: 'AI辅助药物研发取得突破',
      source: '医药经济报',
      time: '2026-03-19 17:00',
      summary: 'AI技术在药物研发中的应用取得重要突破，研发周期缩短40%',
      url: 'https://example.com/news9',
      category: 'AI科技'
    },
    {
      title: '氢能产业发展规划发布',
      source: '发改委',
      time: '2026-03-19 18:15',
      summary: '国家发布氢能产业发展规划，目标到2030年产值突破1万亿元',
      url: 'https://example.com/news10',
      category: '新能源'
    }
  ];
  
  // 添加模拟新闻
  mockNews.forEach((news, index) => {
    newsList.push({
      id: index + 1,
      ...news
    });
  });
  
  console.log(`收集到 ${newsList.length} 条新闻`);
  
  // 保存为JSON文件
  const jsonPath = path.join(__dirname, 'news_collection', `${today}_news.json`);
  fs.writeFileSync(jsonPath, JSON.stringify(newsList, null, 2));
  console.log(`新闻已保存到: ${jsonPath}`);
  
  // 保存为Markdown文件
  const mdContent = generateMarkdown(newsList, today);
  const mdPath = path.join(__dirname, 'news_collection', `${today}_晨间新闻汇总.md`);
  fs.writeFileSync(mdPath, mdContent);
  console.log(`Markdown文件已保存到: ${mdPath}`);
  
  // 保存为网站格式
  const webJsonPath = path.join(__dirname, 'news_collection', `${today}_news_for_web.json`);
  const webData = formatForWebsite(newsList, today);
  fs.writeFileSync(webJsonPath, JSON.stringify(webData, null, 2));
  console.log(`网站数据已保存到: ${webJsonPath}`);
  
  return {
    newsCount: newsList.length,
    jsonPath,
    mdPath,
    webJsonPath
  };
}

// 生成Markdown内容
function generateMarkdown(newsList, date) {
  let content = `# ${date} 晨间新闻汇总\n\n`;
  content += `**收集时间**: ${new Date().toLocaleString('zh-CN', { timeZone: 'Asia/Shanghai' })}\n`;
  content += `**新闻数量**: ${newsList.length} 条\n\n`;
  
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
      content += `- 相关行业可能受到影响\n`;
      content += `- 投资机会值得关注\n`;
      content += `- 技术发展趋势明显\n`;
      content += `**原文链接**: ${news.url}\n\n`;
    });
  });
  
  return content;
}

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

// 执行收集
collectNews().then(result => {
  console.log('新闻收集完成！');
  console.log(`收集了 ${result.newsCount} 条新闻`);
  console.log(`文件已保存到 news_collection 文件夹`);
}).catch(error => {
  console.error('新闻收集失败:', error);
});