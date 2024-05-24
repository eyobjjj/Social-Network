import react from "react";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import Login from "./pages/auth/Login";
import Register from "./pages/auth/Register";
import NotFound from "./components/NotFound";
import ProtectedRoute from "./components/ProtectedRoute";

import Home from "./pages/home/home";
import Allpost from "./pages/home/allpost";
import PostDetail from "./pages/detail/post";
import Profile from "./pages/profile/profile";
import ChatRoom from "./pages/chat/chatroom";
import Setting from "./pages/setting/Settings";
import Upload from "./pages/upload/upload";
import Dashboard from "./pages/dashboard/dashboard";
import Short from "./pages/short/short";
import Save from "./pages/save/save";
import Search from "./pages/search/search";

import Check from "./check";

import { DarkThemeToggle, Flowbite } from "flowbite-react";

import { USER } from "/src/constants";
const username = localStorage.getItem(USER);

function Logout() {
  localStorage.clear();
  return <Navigate to="/login" />;
}
function RegisterAndLogout() {
  localStorage.clear();
  return <Register />;
}

function App() {
  return (
    <>
      <Flowbite>
        <div className="antialiased bg-gray-50 dark:bg-gray-900">
          <BrowserRouter>
            <Routes>
              <Route
                index
                element={
                  <ProtectedRoute>
                    {" "}
                    <Home />
                  </ProtectedRoute>
                }
              />
              <Route
                path="post"
                element={
                  <ProtectedRoute>
                    {" "}
                    <Allpost />
                  </ProtectedRoute>
                }
              />
              <Route
                path="post/:id"
                element={
                  <ProtectedRoute>
                    {" "}
                    <PostDetail />{" "}
                  </ProtectedRoute>
                }
              />
              <Route
                path="/:id"
                element={
                  <ProtectedRoute>
                    {" "}
                    <Profile />{" "}
                  </ProtectedRoute>
                }
              />
              <Route
                path="chat"
                element={
                  <ProtectedRoute>
                    {" "}
                    <Navigate to={`${username}`} />{" "}
                  </ProtectedRoute>
                }
              />
              <Route
                path="chat/:id"
                element={
                  <ProtectedRoute>
                    {" "}
                    <ChatRoom />{" "}
                  </ProtectedRoute>
                }
              />
              <Route
                path="settings"
                element={
                  <ProtectedRoute>
                    {" "}
                    <Setting />{" "}
                  </ProtectedRoute>
                }
              />
              <Route
                path="upload"
                element={
                  <ProtectedRoute>
                    {" "}
                    <Upload />{" "}
                  </ProtectedRoute>
                }
              />
              <Route
                path="dashboard"
                element={
                  <ProtectedRoute>
                    {" "}
                    <Dashboard />{" "}
                  </ProtectedRoute>
                }
              />
              <Route
                path="short"
                element={
                  <ProtectedRoute>
                    {" "}
                    <Short />{" "}
                  </ProtectedRoute>
                }
              />
              <Route
                path="save"
                element={
                  <ProtectedRoute>
                    {" "}
                    <Save />{" "}
                  </ProtectedRoute>
                }
              />
              <Route
                path="search/:id"
                element={
                  <ProtectedRoute>
                    {" "}
                    <Search />{" "}
                  </ProtectedRoute>
                }
              />

              <Route
                path="/logout"
                element={
                  <ProtectedRoute>
                    {" "}
                    <Logout />{" "}
                  </ProtectedRoute>
                }
              />

              <Route path="/login" element={<Login />} />
              <Route path="/register" element={<RegisterAndLogout />} />
              <Route path="/check" element={<Check />} />
              <Route path="*" element={<NotFound />} />
            </Routes>
          </BrowserRouter>
        </div>
      </Flowbite>
    </>
  );
}

export default App;

{
  /* <Routes>
    <Route path='/' element={<Home />} />
    <Route path='about' element={<About />} />
    <Route path='posts' element={<Posts />}>
        <Route path='new' element={<NewPost />} />
        <Route path=':postId' element={<Post />}>
            <Route index element={<PostIndex />} />
            <Route path='comments' element={<Comments />} />
        </Route>
    </Route>
</Routes> 


<Route path="post/:id" element={ <ProtectedRoute> <PostDetail /> </ProtectedRoute> } />



*/
}
