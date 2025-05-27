export interface Room {
  room_no: string
  roomAmount: number
  durationType: string
  roomType: string
  roomStatus: string
  imageUrl?: string
  roomConfig?: string[]
  status?: string
}

export interface RoomInterface {
  room_no: string;
  room_status: string;
  room_type: string;
  room_amount: number;
  duration_type: string;
  room_config: string[];
}