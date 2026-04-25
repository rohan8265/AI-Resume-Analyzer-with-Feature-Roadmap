import { useState } from "react";
import axios from "axios";

export default function Register() {
    const [name, setName] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");

    const handleRegister = async () => {
        try {
            const res = await axios.post(
                "http://127.0.0.1:8000/api/auth/register",
                {
                    name,
                    email,
                    password,
                }
            );

            alert("Registered Successfully");
            console.log(res.data);

        } catch (error) {
            console.error(error);
            alert("Registration Failed");
        }
    };

    return (
        <div style={{ padding: "20px" }}>
            <h2>Create Account</h2>

            <input
                placeholder="Full Name"
                onChange={(e) => setName(e.target.value)}
            /><br /><br />

            <input
                placeholder="Email"
                onChange={(e) => setEmail(e.target.value)}
            /><br /><br />

            <input
                type="password"
                placeholder="Password"
                onChange={(e) => setPassword(e.target.value)}
            /><br /><br />

            <button onClick={handleRegister}>
                Create Account
            </button>
        </div>
    );
}