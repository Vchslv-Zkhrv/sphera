import { BrowserRouter, Route, Routes, Navigate } from "react-router-dom";
import Admin from "./admin/Admin";
import User from "./user/User";

function App() {
  return (
    <BrowserRouter>
        <Routes>
            <Route path="/admin" element={<Admin/>}/>
            <Route path="/*" element={<User/>}/>
            <Route path="*" element={<Navigate to="/"/>}/>
        </Routes>
    </BrowserRouter>
  );
}

export default App;
