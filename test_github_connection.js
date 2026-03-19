#!/usr/bin/env node
/**
 * 测试GitHub连接和推送
 */

const { execSync } = require('child_process');

console.log('🔍 测试GitHub连接状态');
console.log('='.repeat(40));

try {
    // 测试Git远程连接
    console.log('\n1. 测试Git远程连接...');
    const remoteUrl = execSync('git remote get-url origin', { encoding: 'utf8' }).trim();
    console.log(`✅ 远程仓库: ${remoteUrl}`);
    
    // 测试网络连接
    console.log('\n2. 测试GitHub网络连接...');
    try {
        execSync('ping -n 2 github.com', { stdio: 'ignore' });
        console.log('✅ GitHub网络连接正常');
    } catch (error) {
        console.log('⚠️ GitHub网络连接可能有问题');
    }
    
    // 检查本地提交状态
    console.log('\n3. 检查本地提交状态...');
    const status = execSync('git status --porcelain', { encoding: 'utf8' });
    if (status.trim()) {
        console.log('⚠️ 有未提交的更改:');
        console.log(status);
    } else {
        console.log('✅ 所有更改已提交');
    }
    
    // 检查本地和远程差异
    console.log('\n4. 检查本地和远程差异...');
    try {
        execSync('git fetch origin', { stdio: 'ignore' });
        const diff = execSync('git log origin/main..main --oneline', { encoding: 'utf8' });
        if (diff.trim()) {
            console.log('✅ 有需要推送的提交:');
            console.log(diff);
        } else {
            console.log('✅ 本地和远程已同步');
        }
    } catch (error) {
        console.log('❌ 无法获取远程状态');
    }
    
    // 测试推送（不实际执行）
    console.log('\n5. 测试推送命令...');
    console.log('📋 推送命令: git push origin main');
    console.log('📋 强制推送: git push -u origin main --force');
    
    console.log('\n' + '='.repeat(40));
    console.log('🎯 建议操作:');
    console.log('1. 如果网络正常，尝试强制推送');
    console.log('2. 检查GitHub Token权限');
    console.log('3. 验证仓库访问权限');
    console.log('4. 等待网络恢复后重试');
    
} catch (error) {
    console.log(`❌ 测试失败: ${error.message}`);
}