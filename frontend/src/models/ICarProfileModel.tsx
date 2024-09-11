export interface ICarProfileModel {
    id: number
    city: string,
    region: string,
    description: string,
    color: string,
    owner_amount: number,
    mileage: number,
    engine_type: string,
    engine_volume: number,
    transmission_type: string,
    body: string,
    created_at: Date,
    updated_at: Date,
}