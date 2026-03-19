// 新闻网站交互功能
document.addEventListener('DOMContentLoaded', function() {
    console.log('🦞 小龙虾新闻网站已加载 | 2026年3月18日');
    
    // 1. 更新时间显示
    updateTimeDisplay();
    
    // 2. 初始化新闻卡片交互
    initNewsCards();
    
    // 3. 初始化重要性筛选
    initImportanceFilter();
    
    // 4. 添加打印功能
    addPrintButton();
    
    // 5. 添加模块折叠功能
    addModuleToggle();
    
    // 6. 添加回到顶部按钮
    addBackToTopButton();
});

// 更新时间显示
function updateTimeDisplay() {
    const timeElement = document.querySelector('.time');
    if (timeElement) {
        const now = new Date();
        const options = { 
            year: 'numeric', 
            month: '2-digit', 
            day: '2-digit',
            hour: '2-digit',
            minute: '2-digit',
            hour12: false,
            timeZone: 'Asia/Shanghai'
        };
        const beijingTime = now.toLocaleString('zh-CN', options);
        timeElement.innerHTML = `<i class="fas fa-clock"></i> 更新于 ${beijingTime}`;
    }
}

// 初始化新闻卡片交互
function initNewsCards() {
    const newsCards = document.querySelectorAll('.news-card, .insight-card, .optimization-card');
    
    newsCards.forEach(card => {
        // 点击卡片展开/收起详情
        card.addEventListener('click', function(e) {
            // 防止点击链接时触发
            if (e.target.tagName === 'A') return;
            
            this.classList.toggle('expanded');
            
            // 添加视觉反馈
            if (this.classList.contains('expanded')) {
                this.style.boxShadow = '0 10px 25px rgba(0,0,0,0.15)';
                this.style.transform = 'scale(1.02)';
            } else {
                this.style.boxShadow = '';
                this.style.transform = '';
            }
        });
        
        // 鼠标悬停效果
        card.addEventListener('mouseenter', function() {
            if (!this.classList.contains('expanded')) {
                this.style.transform = 'translateX(10px)';
            }
        });
        
        card.addEventListener('mouseleave', function() {
            if (!this.classList.contains('expanded')) {
                this.style.transform = '';
            }
        });
    });
    
    console.log(`✅ 已初始化 ${newsCards.length} 个新闻卡片交互`);
}

// 初始化重要性筛选
function initImportanceFilter() {
    // 创建筛选控件
    const filterContainer = document.createElement('div');
    filterContainer.className = 'importance-filter';
    filterContainer.innerHTML = `
        <div style="margin: 20px 0; padding: 15px; background: white; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.05);">
            <h4 style="margin-bottom: 10px; color: #2E7D32;"><i class="fas fa-filter"></i> 重要性筛选</h4>
            <div style="display: flex; gap: 10px; flex-wrap: wrap;">
                <button class="filter-btn active" data-importance="all">全部新闻</button>
                <button class="filter-btn" data-importance="5">★★★★★ (最高)</button>
                <button class="filter-btn" data-importance="4">★★★★☆ (高)</button>
                <button class="filter-btn" data-importance="3">★★★☆☆ (中)</button>
            </div>
        </div>
    `;
    
    // 插入到页面标题后
    const pageHeader = document.querySelector('.page-header');
    if (pageHeader) {
        pageHeader.parentNode.insertBefore(filterContainer, pageHeader.nextSibling);
    }
    
    // 添加筛选功能
    const filterButtons = document.querySelectorAll('.filter-btn');
    filterButtons.forEach(button => {
        button.addEventListener('click', function() {
            // 更新按钮状态
            filterButtons.forEach(btn => btn.classList.remove('active'));
            this.classList.add('active');
            
            // 筛选新闻
            const importance = this.dataset.importance;
            filterNewsByImportance(importance);
        });
    });
}

// 根据重要性筛选新闻
function filterNewsByImportance(importance) {
    const newsCards = document.querySelectorAll('.news-card');
    let visibleCount = 0;
    
    newsCards.forEach(card => {
        const importanceElement = card.querySelector('.news-importance');
        if (!importanceElement) return;
        
        const cardImportance = importanceElement.textContent;
        let shouldShow = false;
        
        switch(importance) {
            case 'all':
                shouldShow = true;
                break;
            case '5':
                shouldShow = cardImportance.includes('★★★★★');
                break;
            case '4':
                shouldShow = cardImportance.includes('★★★★☆');
                break;
            case '3':
                shouldShow = cardImportance.includes('★★★☆☆');
                break;
        }
        
        if (shouldShow) {
            card.style.display = 'block';
            visibleCount++;
            // 添加显示动画
            card.style.animation = 'fadeInUp 0.5s ease-out';
        } else {
            card.style.display = 'none';
        }
    });
    
    console.log(`🔍 筛选结果: 显示 ${visibleCount} 条新闻 (重要性: ${importance})`);
}

// 添加打印按钮
function addPrintButton() {
    const printButton = document.createElement('button');
    printButton.innerHTML = '<i class="fas fa-print"></i> 打印本页';
    printButton.className = 'print-button';
    printButton.style.cssText = `
        position: fixed;
        bottom: 20px;
        right: 20px;
        background: #4CAF50;
        color: white;
        border: none;
        padding: 12px 20px;
        border-radius: 25px;
        cursor: pointer;
        box-shadow: 0 4px 15px rgba(76, 175, 80, 0.3);
        z-index: 1000;
        font-family: inherit;
        font-weight: 500;
        transition: all 0.3s ease;
        display: flex;
        align-items: center;
        gap: 8px;
    `;
    
    printButton.addEventListener('mouseenter', function() {
        this.style.transform = 'translateY(-3px)';
        this.style.boxShadow = '0 6px 20px rgba(76, 175, 80, 0.4)';
    });
    
    printButton.addEventListener('mouseleave', function() {
        this.style.transform = '';
        this.style.boxShadow = '0 4px 15px rgba(76, 175, 80, 0.3)';
    });
    
    printButton.addEventListener('click', function() {
        window.print();
    });
    
    document.body.appendChild(printButton);
}

// 添加模块折叠功能
function addModuleToggle() {
    const moduleHeaders = document.querySelectorAll('.module-header');
    
    moduleHeaders.forEach(header => {
        const toggleButton = document.createElement('button');
        toggleButton.innerHTML = '<i class="fas fa-chevron-down"></i>';
        toggleButton.className = 'module-toggle';
        toggleButton.style.cssText = `
            background: rgba(255,255,255,0.2);
            border: none;
            color: white;
            width: 30px;
            height: 30px;
            border-radius: 50%;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: all 0.3s ease;
        `;
        
        header.appendChild(toggleButton);
        
        toggleButton.addEventListener('click', function(e) {
            e.stopPropagation();
            const module = header.parentElement;
            const content = module.querySelector('.module-content');
            
            if (content.style.display === 'none') {
                content.style.display = 'block';
                this.innerHTML = '<i class="fas fa-chevron-down"></i>';
                this.style.transform = 'rotate(0deg)';
                // 添加展开动画
                content.style.animation = 'fadeInUp 0.5s ease-out';
            } else {
                content.style.display = 'none';
                this.innerHTML = '<i class="fas fa-chevron-right"></i>';
                this.style.transform = 'rotate(-90deg)';
            }
        });
    });
}

// 添加回到顶部按钮
function addBackToTopButton() {
    const backToTopButton = document.createElement('button');
    backToTopButton.innerHTML = '<i class="fas fa-arrow-up"></i>';
    backToTopButton.className = 'back-to-top';
    backToTopButton.style.cssText = `
        position: fixed;
        bottom: 70px;
        right: 20px;
        background: #2E7D32;
        color: white;
        border: none;
        width: 45px;
        height: 45px;
        border-radius: 50%;
        cursor: pointer;
        box-shadow: 0 4px 15px rgba(46, 125, 50, 0.3);
        z-index: 1000;
        font-size: 1.2rem;
        transition: all 0.3s ease;
        opacity: 0;
        visibility: hidden;
    `;
    
    document.body.appendChild(backToTopButton);
    
    // 滚动显示/隐藏按钮
    window.addEventListener('scroll', function() {
        if (window.pageYOffset > 300) {
            backToTopButton.style.opacity = '1';
            backToTopButton.style.visibility = 'visible';
            backToTopButton.style.transform = 'translateY(0)';
        } else {
            backToTopButton.style.opacity = '0';
            backToTopButton.style.visibility = 'hidden';
            backToTopButton.style.transform = 'translateY(10px)';
        }
    });
    
    // 点击回到顶部
    backToTopButton.addEventListener('click', function() {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
    
    // 鼠标悬停效果
    backToTopButton.addEventListener('mouseenter', function() {
        this.style.transform = 'translateY(-5px)';
        this.style.boxShadow = '0 6px 20px rgba(46, 125, 50, 0.4)';
    });
    
    backToTopButton.addEventListener('mouseleave', function() {
        this.style.transform = '';
        this.style.boxShadow = '0 4px 15px rgba(46, 125, 50, 0.3)';
    });
}

// 添加键盘快捷键
document.addEventListener('keydown', function(e) {
    // Ctrl + P: 打印
    if (e.ctrlKey && e.key === 'p') {
        e.preventDefault();
        window.print();
    }
    
    // Esc: 关闭所有展开的卡片
    if (e.key === 'Escape') {
        const expandedCards = document.querySelectorAll('.news-card.expanded, .insight-card.expanded, .optimization-card.expanded');
        expandedCards.forEach(card => {
            card.classList.remove('expanded');
            card.style.boxShadow = '';
            card.style.transform = '';
        });
    }
    
    // 数字键1-5: 跳转到对应模块
    if (e.key >= '1' && e.key <= '5') {
        const modules = document.querySelectorAll('.news-module');
        const index = parseInt(e.key) - 1;
        if (modules[index]) {
            modules[index].scrollIntoView({ behavior: 'smooth' });
        }
    }
});

// 页面加载完成提示
window.addEventListener('load', function() {
    console.log('✅ 页面加载完成，所有资源已就绪');
    
    // 添加加载完成动画
    document.body.style.opacity = '0';
    document.body.style.transition = 'opacity 0.5s ease';
    
    setTimeout(() => {
        document.body.style.opacity = '1';
    }, 100);
});