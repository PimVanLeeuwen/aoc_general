import { HashRouter, Routes, Route } from 'react-router-dom'
import { PyodideProvider } from './context/PyodideContext'
import { SolutionsProvider } from './context/SolutionsContext'
import Layout from './components/Layout'
import HomePage from './pages/HomePage'
import SolutionPage from './pages/SolutionPage'
import TechniquesPage from './pages/TechniquesPage'

export default function App() {
  return (
    <PyodideProvider>
      <SolutionsProvider>
        <HashRouter>
          <Layout>
            <Routes>
              <Route path="/" element={<HomePage />} />
              <Route path="/techniques" element={<TechniquesPage />} />
              <Route path="/:year/:day" element={<SolutionPage />} />
            </Routes>
          </Layout>
        </HashRouter>
      </SolutionsProvider>
    </PyodideProvider>
  )
}
