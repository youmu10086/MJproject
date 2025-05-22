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
    balance: number
    resideTimePeriod: string[]
    status: string
    user_id?: string
}