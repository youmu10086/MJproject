export interface Customer {
    cno: string
    name: string
    idCardNo: string
    mobile: string
    gender: string
    roomNo: string
    checkOutTime: Date | null
    checkInTime: Date | null
    image: string
    imageUrl: string
    balance: number | null  // 修改这一行，从 number 改为 number | null
    resideTimePeriod: string[]
    status: string
}
// 客户模型接口定义
export interface CustomerInterface {
    cno: string; // 客户编号（主键）
    name: string; // 客户姓名
    idCardNo: string; // 身份证号
    mobile: string; // 手机号码
    gender: string; // 性别
    roomNo: string; // 房间号
    checkInTime: Date | null; // 入住时间
    checkOutTime: Date | null; // 退房时间（可为null）
    image: string
    imageUrl: string
    resideTimePeriod: string; // 居住时间段
    balance: number | null;
    status: string; // 状态
}

export enum CustomerDialogStatus {
    NONE = 'none',           // 无状态
    EDIT = 'edit',           // 修改状态
    VIEW = 'view',           // 查看状态
    ADD = 'add',             // 添加状态
    RENEWAL = 'renewal',      // 续租状态
    CHECKINFORSERVED = 'checkInForServed', // 预订顾客办理入住
    CUSTOMERRSERVED = 'customerServed', // 顾客办理入住
}