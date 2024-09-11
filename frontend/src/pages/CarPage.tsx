import React from 'react';
import ChatComponent from "../components/ChatComponent";
import CarsComponent from "../components/CarsComponent";
import CarFormComponent from "../components/CarFormComponent";

const CarPage = () => {
    return (
        <div>
            <CarFormComponent/>
            <hr/>
            <CarsComponent/>
            <hr/>
            <ChatComponent/>
        </div>
    );
};

export default CarPage;