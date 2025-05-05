/**
 * 将 ISO 8601 格式的字符串转换为格式化的日期字符串
 * @param dateString ISO 8601 格式的日期字符串
 * @returns 格式化后的日期字符串，例如 "2023年5月4日12时"，如果输入无效则返回 "无效的日期"
 */
export const formatDate = (dateString: string): string => {
    if (!dateString || typeof dateString !== 'string') return '无效的日期';

    const date = new Date(dateString);

    if (!isNaN(date.getTime())) {
        const year = date.getUTCFullYear();
        const month = date.getUTCMonth() + 1;
        const day = date.getUTCDate();
        const hours = date.getUTCHours();

        return `${year}年${month}月${day}日${hours}时`;
    } else {
        return '无效的日期';
    }
};

/**
 * 格式化住宿时间
 * @param beginTime 开始时间
 * @param endTime 结束时间
 * @returns 格式化后的住宿时间字符串，例如 "2023年5月4日12时到2023年5月5日12时"，如果输入无效则返回 "无效的时间范围"
 */
export const formatResideTime = (beginTime: string, endTime: string): string => {
    if (!beginTime || !endTime || typeof beginTime !== 'string' || typeof endTime !== 'string') {
        return '无效的时间范围';
    }

    const formattedBeginTime = formatDate(beginTime);
    const formattedEndTime = formatDate(endTime);

    if (formattedBeginTime === '无效的日期' || formattedEndTime === '无效的日期') {
        return '无效的时间范围';
    }

    return `${formattedBeginTime}到${formattedEndTime}`;
};

/**
 * 处理居住时间字符串，将其转换为数组
 * @param item 包含 `resideTimePeriod` 属性的对象
 * @returns 转换后的数组，如果解析失败则返回空数组
 */
export const processResideTimePeriod = (item: { resideTimePeriod: any }): string[] => {
    let resideTimePeriodString = item.resideTimePeriod;

    if (!resideTimePeriodString || typeof resideTimePeriodString !== 'string') {
        console.error('Invalid resideTimePeriodString:', resideTimePeriodString);
        return [];
    }

    // 替换单引号为双引号
    resideTimePeriodString = resideTimePeriodString.replace(/'/g, '"');

    try {
        // 使用 JSON.parse 将字符串转换为数组
        return JSON.parse(resideTimePeriodString);
    } catch (error) {
        console.error('Error parsing resideTimePeriodString:', error);
        return [];
    }
};