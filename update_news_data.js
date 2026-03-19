const fs = require('fs');
const path = require('path');

function updateNewsData() {
    console.log("🔄 开始更新新闻数据...");
    
    // 读取今日新闻
    const todayNewsPath = path.join(__dirname, 'news_collection', '2026-03-19_news_for_web.json');
    
    if (!fs.existsSync(todayNewsPath)) {
        console.log(`❌ 未找到今日新闻文件: ${todayNewsPath}`);
        return false;
    }
    
    const todayNews = JSON.parse(fs.readFileSync(todayNewsPath, 'utf8'));
    
    // 读取现有新闻数据
    const newsDataPath = path.join(__dirname, 'news-data.json');
    if (!fs.existsSync(newsDataPath)) {
        console.log(`❌ 未找到新闻数据文件: ${newsDataPath}`);
        return false;
    }
    
    const newsData = JSON.parse(fs.readFileSync(newsDataPath, 'utf8'));
    
    // 更新元数据
    const now = new Date();
    const beijingTime = new Date(now.getTime() + 8 * 60 * 60 * 1000);
    const formattedTime = beijingTime.toISOString().replace('Z', '+08:00');
    
    newsData.metadata.generated_at = formattedTime;
    newsData.metadata.source = "自动更新系统";
    newsData.metadata.total_news = todayNews.news.length;
    newsData.metadata.categories = todayNews.categories;
    newsData.metadata.version = "2.0";
    newsData.metadata.next_update = "2026-03-20 08:30";
    newsData.metadata.test_purpose = "正式自动更新 - 2026年3月19日";
    
    // 清空现有新闻，添加今日新闻
    newsData.news = [];
    
    // 转换今日新闻格式
    const categoryMap = {
        'AI科技': 'ai',
        '新能源': 'energy',
        '商业航天': 'space',
        '国际财经': 'international',
        '经济金融': 'finance'
    };
    
    todayNews.news.forEach((item, i) => {
        // 确定类别
        const category = categoryMap[item.category] || 'general';
        
        // 创建新闻条目
        const newsItem = {
            id: i + 1,
            order: i,
            title: item.title,
            category: category,
            time: item.time,
            subject: item.source || '未指定',
            event: item.summary,
            impact: [
                `来源: ${item.source}`,
                `类别: ${item.category}`,
                `发布时间: ${item.time}`
            ],
            link: item.url
        };
        newsData.news.push(newsItem);
    });
    
    // 保存更新后的数据
    fs.writeFileSync(newsDataPath, JSON.stringify(newsData, null, 2), 'utf8');
    
    console.log(`✅ 成功更新新闻数据文件`);
    console.log(`📊 新闻总数: ${newsData.news.length}`);
    console.log(`📁 类别: ${todayNews.categories.join(', ')}`);
    console.log(`⏰ 更新时间: ${newsData.metadata.generated_at}`);
    
    return true;
}

// 执行更新
if (updateNewsData()) {
    console.log("🎉 新闻数据更新完成！");
} else {
    console.log("❌ 新闻数据更新失败");
    process.exit(1);
}