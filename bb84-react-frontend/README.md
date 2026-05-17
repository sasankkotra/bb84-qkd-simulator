# BB84 Quantum Key Distribution - React Frontend

Modern React dashboard for the BB84 QKD Simulator with real-time analytics and visualization.

## Features

- ⚡ **Fast Development** - Vite + React with HMR
- 🎨 **Beautiful UI** - Tailwind CSS with custom theme
- 📊 **Live Analytics** - Interactive charts with Recharts
- 🔐 **Real-time Updates** - Server-Sent Events (SSE) streaming
- 📱 **Responsive Design** - Works on all screen sizes
- 🎯 **Type-Safe** - Full TypeScript support
- 🔄 **State Management** - Zustand for simple, powerful state

## Project Structure

```
src/
├── main.tsx              # Entry point
├── index.css             # Tailwind styles
├── api/
│   └── client.ts         # API client & types
├── store/
│   └── simulation.ts     # Zustand store
└── components/
    ├── Dashboard.tsx     # Main dashboard layout
    ├── ControlPanel.tsx  # Simulation controls
    ├── AnalyticsPanel.tsx # Charts & graphs
    ├── ResultsPanel.tsx   # Results display
    └── SimulationButton.tsx # Run/Reset buttons
```

## Getting Started

### Prerequisites
- Node.js 18+ (with npm)
- FastAPI backend running on `http://localhost:8000`

### Installation

```bash
cd bb84-react-frontend
npm install
```

### Development

```bash
npm run dev
```

Visit `http://localhost:3000` in your browser.

### Build for Production

```bash
npm run build
npm run preview
```

## Configuration

The app looks for the FastAPI backend at `http://localhost:8000/api`

To change this, set the environment variable:
```bash
REACT_APP_API_URL=http://your-backend-url/api npm run dev
```

## API Integration

The frontend connects to these endpoints:
- `GET /api/simulate/stream` - Stream simulation results via SSE

### Example request:
```
GET /api/simulate/stream?num_qubits=1000&eve_active=false&noise_prob=0.05&seed=42
```

The backend sends JSON events:
```json
event: progress
data: {"progress": 0.25}

event: done
data: {"qber": 4.2, "matched": 512, "total": 1000, ...}
```

## Customization

### Colors & Theme
Edit `tailwind.config.ts`:
```typescript
extend: {
  colors: {
    'cyan-accent': '#0284C7',
    'green-secure': '#16A34A',
    'purple-key': '#7C3AED',
  },
},
```

### Chart Colors
Edit `src/components/AnalyticsPanel.tsx`:
```typescript
const COLORS = {
  secure: '#16A34A',
  compromised: '#EF4444',
  // ...
}
```

## Troubleshooting

**CORS Errors?**
- Make sure FastAPI backend is running with CORS enabled
- Check `frontend_web/main.py` includes proper CORS middleware

**Blank Page?**
- Check browser console for errors
- Verify backend is running on port 8000
- Try clearing browser cache & restart dev server

**Connection Refused?**
- Ensure FastAPI server is running: `python -m uvicorn frontend_web.main:app --port 8000`
- Check firewall settings

## Deploy to Vercel

```bash
npm run build
vercel deploy
```

Set environment variable in Vercel dashboard:
```
REACT_APP_API_URL=https://your-backend-url.com/api
```

## Technologies Used

- **React 18** - UI framework
- **Vite** - Build tool
- **TypeScript** - Type safety
- **Tailwind CSS** - Styling
- **Recharts** - Charts & visualizations
- **Zustand** - State management
- **Axios** - HTTP client

## License

MIT
