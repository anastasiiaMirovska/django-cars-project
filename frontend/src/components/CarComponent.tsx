import React, {FC} from 'react';
import {ICarModel} from "../models/ICarModel";
import {IModelModel} from "../models/ICarModelModel";
import {IUserModel} from "../models/IUserModel";

const CarComponent: FC<ICarModel> = (car) => {

    return (
        <div>
            <hr/>
            <ul> Car {car.id}:</ul>
             <li>model: {car.model.name}</li>
             <li>brand: {car.model.brand.name}</li>
             <li>year: {car.year}</li>
             <li>price:{car.price.initial_price}</li>
             <li>currency: {car.price.initial_currency}</li>
             <li>is_used: {car.is_used}</li>
             <li>is_active: {car.is_active}</li>
             <li>edit_attempts: {car.edit_attempts}</li>
             <li>user: {car.user.id}</li>
            <hr/>
        </div>
    );
};

export default CarComponent;