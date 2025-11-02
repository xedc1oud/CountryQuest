from datetime import datetime, date

from sqlalchemy import BigInteger, DateTime, ForeignKey, String, Integer, func, ARRAY, Date
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker, AsyncAttrs
from sqlalchemy.pool import NullPool


class Base(AsyncAttrs, DeclarativeBase):
    pass


class Database:
    def __init__(self, url: str):
        self.engine = create_async_engine(url, poolclass=NullPool, echo=False)
        self.async_session = async_sessionmaker(
            self.engine, 
            class_=AsyncSession, 
            expire_on_commit=False
        )
    
    async def create_tables(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    
    async def drop_tables(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
    
    async def close(self):
        await self.engine.dispose()
    
    def get_session(self) -> AsyncSession:
        return self.async_session()
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()


class User(Base):
    __tablename__ = 'users'
    
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    username: Mapped[str | None] = mapped_column(String(255), nullable=True)
    telegram: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())
    admin: Mapped[int] = mapped_column(Integer, default=0)
    
    def __repr__(self) -> str:
        return (f'User(id={self.id!r}, name={self.name!r}, username={self.username!r}, '
                f'telegram={self.telegram!r}, created_at={self.created_at!r})')


class Country(Base):
    __tablename__ = 'countries'
    
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    uid: Mapped[int] = mapped_column(BigInteger, unique=False, nullable=False, index=True)
    cid: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False, index=True)
    group: Mapped[int] = mapped_column(BigInteger, nullable=False, unique=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    leader: Mapped[str | None] = mapped_column(String(255), nullable=True)
    ideology: Mapped[str | None] = mapped_column(String(255), nullable=True)
    
    def __repr__(self) -> str:
        return (f'Country(id={self.id!r}, uid={self.uid!r}, cid={self.cid!r}, group={self.group!r}, '
                f'name={self.name!r}, leader={self.leader!r}, '
                f'ideology={self.ideology!r})')


class Army(Base):
    __tablename__ = 'army'
    
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    cid: Mapped[int] = mapped_column(Integer, unique=True, nullable=False, index=True)
    
    def __repr__(self) -> str:
        return f'Army(id={self.id!r}, uid={self.cid!r})'


class Economy(Base):
    __tablename__ = 'economy'
    
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    cid: Mapped[int] = mapped_column(Integer, unique=True, nullable=False, index=True)
    gdp: Mapped[int] = mapped_column(BigInteger, default=0)
    population: Mapped[int] = mapped_column(BigInteger, default=0)
    inflation: Mapped[float] = mapped_column(String(50), default="0.0")
    capita: Mapped[int] = mapped_column(default=0)
    debt: Mapped[float] = mapped_column(String(50), default="0.0")
    unemployment: Mapped[float] = mapped_column(String(50), default="0.0")
    exports: Mapped[bool] = mapped_column(default=True)
    imports: Mapped[bool] = mapped_column(default=True)
    budget: Mapped[int] = mapped_column(BigInteger, default=0)
    income: Mapped[int] = mapped_column(BigInteger, default=0)
    expense: Mapped[int] = mapped_column(BigInteger, default=0)
    deficit: Mapped[float] = mapped_column(String(50), default="0.0")
    interest: Mapped[float] = mapped_column(String(50), default="0.0")
    poverty: Mapped[float] = mapped_column(String(50), default="0.0")
    labor: Mapped[float] = mapped_column(String(50), default="0.0")
    migration: Mapped[float] = mapped_column(String(50), default="0.0")
    reverse: Mapped[float] = mapped_column(String(50), default="0.0")
    military_factories: Mapped[int] = mapped_column(BigInteger, default=0)
    factories: Mapped[int] = mapped_column(BigInteger, default=0)
    farms: Mapped[int] = mapped_column(BigInteger, default=0)
    ports: Mapped[int] = mapped_column(BigInteger, default=0)
    centralization_ports: Mapped[bool] = mapped_column(default=False)
    private_business: Mapped[bool] = mapped_column(default=True)
    birth: Mapped[float] = mapped_column(String(50), default="0.0")
    death: Mapped[float] = mapped_column(String(50), default="0.0")
    
    def __repr__(self) -> str:
        return f'Economy(id={self.id!r}, cid={self.uid!r}), gdp={self.gdp!r} ' \
                f'inflation={self.inflation!r}, capita={self.capita!r}) ' \
                f'debt={self.debt!r}, unemployment={self.unemployment!r}) ' \
                f'exports={self.exports!r}, imports={self.imports!r}) ' \
                f'budget={self.budget!r}, income={self.income!r}) ' \
                f'expense={self.expense!r}, deficit={self.deficit!r}) ' \
                f'interest={self.interest!r}, poverty={self.poverty!r}) ' \
                f'labor={self.labor!r}, migration={self.migration!r}) ' \
                f'reverse={self.reverse!r}), military_factories={self.military_factories!r}) ' \
                f'factories={self.factories!r}), farms={self.farms!r}) ' \
                f'ports={self.ports!r}), centralization_ports={self.centralization_ports!r}) ' \
                f'private_business={self.private_business!r}), birth={self.birth!r}), death={self.death!r})'


class History(Base):
    __tablename__ = 'history'
    
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    cid: Mapped[int] = mapped_column(Integer, unique=True, nullable=False, index=True)
    
    def __repr__(self) -> str:
        return f'History(id={self.id!r}, uid={self.cid!r})'


class Science(Base):
    __tablename__ = 'science'
    
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    cid: Mapped[int] = mapped_column(Integer, unique=True, nullable=False, index=True)
    
    def __repr__(self) -> str:
        return f'Science(id={self.id!r}, cid={self.uid!r})'


class Politics(Base):
    __tablename__ = 'politics'
    
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    cid: Mapped[int] = mapped_column(Integer, unique=True, nullable=False, index=True)
    
    def __repr__(self) -> str:
        return f'Politics(id={self.id!r}, uid={self.cid!r})'


class Administry(Base):
    __tablename__ = 'administry'
    
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    cid: Mapped[int] = mapped_column(Integer, unique=True, nullable=False, index=True)
    
    def __repr__(self) -> str:
        return f'Administry(id={self.id!r}, uid={self.cid!r})'
    



class Group(Base):
    __tablename__ = 'groups'
    
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    gid: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    start_date: Mapped[date] = mapped_column(Date, nullable=True)
    current_date: Mapped[date] = mapped_column(Date, nullable=True)
    created_at: Mapped[date] = mapped_column(Date, nullable=True)
    sid: Mapped[int] = mapped_column(BigInteger, unique=False, index=True, nullable=True)
    owner: Mapped[int] = mapped_column(BigInteger, nullable=True)
    admins: Mapped[list[int]] = mapped_column(ARRAY(BigInteger), nullable=False, default=list)
    
    def __repr__(self) -> str:
        return (f'Group(id={self.id!r}, gid={self.gid!r}, name={self.name!r}, ' \
                f'start_date={self.start_date!r}, current_date={self.current_date!r}, ' \
                f'sid={self.sid!r}, admins={self.admins!r})')