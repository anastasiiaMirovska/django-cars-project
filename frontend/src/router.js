import {createBrowserRouter, Navigate} from "react-router-dom";
import MainLayout from "./layouts/MainLayout";
import LogInPage from "./pages/LogInPage";
import CarPage from "./pages/CarPage";

const router = createBrowserRouter([
    {
        path:'', element:<MainLayout/>, children:[
            {
                index: true, element: <Navigate to={'login'}/>
            },
            {
                path: 'login', element: <LogInPage/>
            },
            {
                path: 'cars', element: <CarPage/>
            }
        ]
    }
])

export {
    router
}