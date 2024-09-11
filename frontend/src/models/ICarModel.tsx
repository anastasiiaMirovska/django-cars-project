import {IUserModel} from "./IUserModel";
import {IModelModel} from "./ICarModelModel";
import {IPriceModel} from "./IPriceModel";

export interface ICarModel {
    id: number,
    model: IModelModel,
    year: number,
    price: IPriceModel,
    is_used: boolean,
    is_active: boolean,
    edit_attempts: number,
    user: IUserModel,
    created_at: Date,
    updated_at: Date,
}
