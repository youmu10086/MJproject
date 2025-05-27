import { ElMessageBox, MessageBoxData } from 'element-plus';

/**
 * 显示通用确认对话框
 * @param {string} message - 对话框的提示信息
 * @param {string} title - 对话框的标题
 * @param {Object} options - 可选的配置项
 * @returns {Promise} 返回一个 Promise，用户点击确定时 resolve，点击取消时 reject
 */
const showConfirmDialog = (message: string, title: string = '提示', options: object = {}): Promise<MessageBoxData> => {
    return ElMessageBox.confirm(
        message,
        title,
        {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning',
            center: true,
            ...options, // 合并用户自定义的配置项
        }
    );
};

export default showConfirmDialog;