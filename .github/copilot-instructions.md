# GitHub Copilot Instructions

This repository uses Python 3.13+ and TypeScript/React with strict code quality standards.

## Python Standards

**Environment & Syntax:**
- Python 3.13 with modern syntax: `list[T]`, `dict[K, V]`, `X | None` (not `Optional[X]`)
- Use `@dataclass` from dataclasses for data models

**Style:**
- Ruff for linting/formatting (4-space indent, double quotes, 100 char line length)
- Google-style docstrings for all public APIs
- Organize imports: stdlib → third-party → local

**Typing:**
- Strict type annotations (PyRight/MyPy compatible)
- Annotate all function parameters and return types
- For NumPy: `npt.NDArray[np.float32]`

**Testing:**
- pytest with pytest-asyncio for async tests
- Use `httpx.AsyncClient` for FastAPI endpoint tests
- Descriptive names: `test_<function>_<scenario>_<expected_outcome>`

**FastAPI Patterns:**
- Use dependency injection for shared logic (e.g., `Annotated[AsyncSession, Depends(get_db)]`)
- Return appropriate HTTP status codes
- Handle errors with `HTTPException`

## TypeScript/React Standards

**Core:**
- TypeScript 5+ strict mode
- Functional components with hooks only
- Explicit types for all function params and return values

**Styling:**
- Tailwind CSS for utilities
- MUI components for complex UI
- Avoid inline styles

**Data Management:**
- `@tanstack/react-query` for server state
- Use orval-generated API clients for type-safe backend calls

**Code Quality:**
- ESLint + Prettier
- Keep components < 200 lines
- Extract complex logic to custom hooks

## Quick Examples

**Python dataclass:**
```python
@dataclass
class Portfolio:
    """User investment portfolio."""
    name: str
    cash_balance: Decimal
    user_id: int

    def __post_init__(self) -> None:
        if self.cash_balance < 0:
            raise ValueError("Balance cannot be negative")
```

**FastAPI endpoint:**
```python
@router.post("/", response_model=PortfolioResponse)
async def create_portfolio(
    data: PortfolioCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> Portfolio:
    """Create new portfolio."""
    portfolio = Portfolio(user_id=1, name=data.name, cash_balance=data.initial_cash)
    db.add(portfolio)
    await db.flush()
    return portfolio
```

**React component:**
```tsx
export function PortfolioList({ userId }: { userId: string }) {
  const { data, isLoading } = useQuery({
    queryKey: ["portfolios", userId],
    queryFn: () => fetchPortfolios(userId)
  })

  if (isLoading) return <CircularProgress />
  return <div>{data?.map(p => <PortfolioCard key={p.id} portfolio={p} />)}</div>
}
```
