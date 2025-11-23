import { Layout, Menu } from 'antd'
import { Link, Route, Routes, useNavigate } from 'react-router-dom'
import Dashboard from './pages/Dashboard'
import Portfolio from './pages/Portfolio'
import SecurityDetail from './pages/SecurityDetail'
import Preferences from './pages/Preferences'
import Alerts from './pages/Alerts'
import Login from './pages/Login'
import { useEffect, useState } from 'react'

const { Header, Content } = Layout

function App() {
  const [token, setToken] = useState(localStorage.getItem('token'))
  const navigate = useNavigate()

  useEffect(() => {
    if (!token) {
      navigate('/login')
    }
  }, [token])

  const logout = () => {
    localStorage.removeItem('token')
    setToken(null)
    navigate('/login')
  }

  return (
    <Layout style={{ minHeight: '100vh' }}>
      <Header>
        <Menu theme="dark" mode="horizontal" selectable={false}>
          <Menu.Item key="dashboard"><Link to="/">仪表盘</Link></Menu.Item>
          <Menu.Item key="portfolio"><Link to="/portfolio">投资组合</Link></Menu.Item>
          <Menu.Item key="preferences"><Link to="/preferences">偏好设置</Link></Menu.Item>
          <Menu.Item key="alerts"><Link to="/alerts">提醒</Link></Menu.Item>
          <Menu.Item key="logout" onClick={logout} style={{ float: 'right' }}>退出</Menu.Item>
        </Menu>
      </Header>
      <Content style={{ padding: 24 }}>
        <Routes>
          <Route path="/login" element={<Login onLogin={(t) => { setToken(t); navigate('/'); }} />} />
          <Route path="/" element={<Dashboard />} />
          <Route path="/portfolio" element={<Portfolio />} />
          <Route path="/security/:symbol" element={<SecurityDetail />} />
          <Route path="/preferences" element={<Preferences />} />
          <Route path="/alerts" element={<Alerts />} />
        </Routes>
      </Content>
    </Layout>
  )
}

export default App
