import React, {useEffect, useState} from 'react';
import axios from "axios";
import {ICarModel} from "./models/ICarModel";

const App = () => {

    const [cars, setCars] = useState<ICarModel[]>([])
    useEffect(() => {
        axios.get('/api/cars').then(({data})=>setCars(data.data))
    }, []);
    return (
        <div>
            <h1>Cars</h1>
            {cars.map((car:ICarModel)=><div key={car.id}>{car.id} {car.model.name}</div>)}
        </div>
    );
};

export default App;