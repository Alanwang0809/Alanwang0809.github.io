#!/usr/bin/env python3
"""
小龙虾交易机器人启动脚本
"""

import asyncio
import logging
import sys
import signal
from trading_bot import TradingBot

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('trading_bot.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class TradingBotRunner:
    """交易机器人运行器"""
    
    def __init__(self):
        self.bot = None
        self.shutdown_event = asyncio.Event()
        
    async def run(self):
        """运行交易机器人"""
        logger.info("=" * 60)
        logger.info("🦞 小龙虾交易机器人 v1.0")
        logger.info("=" * 60)
        
        try:
            # 初始化机器人
            self.bot = TradingBot("config.yaml")
            
            # 设置信号处理
            signal.signal(signal.SIGINT, self._signal_handler)
            signal.signal(signal.SIGTERM, self._signal_handler)
            
            # 启动机器人
            await self.bot.start()
            
            # 等待关闭信号
            await self.shutdown_event.wait()
            
            # 优雅关闭
            await self.bot.stop()
            
            logger.info("交易机器人正常关闭")
            
        except Exception as e:
            logger.error(f"交易机器人运行错误: {e}", exc_info=True)
            
        finally:
            # 确保资源清理
            if self.bot and self.bot.is_running:
                await self.bot.stop()
    
    def _signal_handler(self, signum, frame):
        """信号处理函数"""
        logger.info(f"收到关闭信号: {signum}")
        self.shutdown_event.set()
    
    def print_banner(self):
        """打印横幅"""
        banner = """
        ╔══════════════════════════════════════════════════════╗
        ║                                                      ║
        ║      🦞 小 龙 虾 交 易 机 器 人 🦞                  ║
        ║                                                      ║
        ║      版本: 1.0.0 | 模式: 专业交易助手                ║
        ║                                                      ║
        ║      功能:                                           ║
        ║      • 多市场监控 (股票/加密货币)                   ║
        ║      • 智能技术分析                                 ║
        ║      • 自动交易执行                                 ║
        ║      • 实时风险管理                                 ║
        ║      • 性能分析报告                                 ║
        ║                                                      ║
        ╚══════════════════════════════════════════════════════╝
        """
        print(banner)

async def main():
    """主函数"""
    runner = TradingBotRunner()
    runner.print_banner()
    
    # 运行机器人
    await runner.run()

if __name__ == "__main__":
    # 检查Python版本
    import sys
    if sys.version_info < (3, 7):
        print("错误: 需要Python 3.7或更高版本")
        sys.exit(1)
    
    # 运行
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n用户中断，正在关闭...")
    except Exception as e:
        print(f"致命错误: {e}")
        sys.exit(1)