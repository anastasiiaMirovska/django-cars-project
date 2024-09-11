import React from 'react';
import {useForm} from "react-hook-form";
import {carService} from "../services/carService";
import {ICarModel} from "../models/ICarModel";
import {IUserModel} from "../models/IUserModel";

const CarFormComponent = () => {
    const {register, handleSubmit, reset}= useForm()
    const save = async(car:any)=>{
        await carService.create(car);
        reset()
    }

    return (
        <form onSubmit={handleSubmit(save)}>
            <input type="text" placeholder={'brand'} {...register('brand')}/>
            <input type="text" placeholder={'price'} {...register('price')}/>
            <input type="text" placeholder={'year'} {...register('year')}/>
            <input type="text" placeholder={'body_type'} {...register('body_type')}/>
            <button>Save</button>
        </form>
    );
};

export default CarFormComponent;