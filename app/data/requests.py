from typing import Optional, List
from datetime import date
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from .models import User, Country, Economy, Group

class UserRequest:
    def __init__(self, session: AsyncSession):
        self.session = session
        
    async def add_user(self, 
                    telegram: int, 
                    username: Optional[str] = None,
                    name: Optional[str] = None) -> User:
        user = User(
            telegram=telegram,
            username=username,
            name=name
        )
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user
    
    async def get_user(self, telegram: int) -> Optional[User]:
        result = await self.session.execute(
            select(User).where(User.telegram == telegram)
        )
        return result.scalars().first()
    
    async def update(self, **kwargs) -> Optional[User]:
        stmt = update(User).where(User.telegram == kwargs['telegram']).values(**kwargs).returning(User)
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.scalars().first()
    

class CountryRequest:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def add_country(
        self,
        uid: int,
        cid: int,
        name: str,
        group: int,
        leader: Optional[str] = None,
        population: Optional[int] = None,
        ideology: Optional[str] = None,
        army: Optional[int] = None,
        economy: Optional[int] = None,
        history: Optional[int] = None,
        science: Optional[int] = None,
        politics: Optional[int] = None,
        administry: Optional[int] = None
    ) -> Country:
        country = Country(
            uid=uid,
            cid=cid,
            name=name,
            leader=leader,
            group=group,
            population=population,
            ideology=ideology,
            army=army,
            economy=economy,
            history=history,
            science=science,
            politics=politics,
            administry=administry
        )
        self.session.add(country)
        await self.session.commit()
        await self.session.refresh(country)
        return country
    
    async def get_country(self, uid: int, group: int) -> Optional[Country]:
        result = await self.session.execute(
            select(Country).where(Country.uid == uid, Country.group == group)
        )
        return result.scalars().first()
    
    async def update(self, **kwargs) -> Optional[Country]:
        stmt = update(Country).where(Country.cid == kwargs['cid']).values(**kwargs).returning(Country)
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.scalars().first()
    
    async def delete_country(self, cid: int) -> bool:
        stmt = delete(Country).where(Country.cid == cid)
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.rowcount > 0
    
    
class EconomyRequest:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def add_economy(
        self,
        cid: int,
        gdp: Optional[float] = None,
        population: Optional[float] = None,
        inflation: Optional[float] = None,
        capita: Optional[float] = None,
        debt: Optional[float] = None,
        unemployment: Optional[float] = None,
        exports: Optional[float] = None,
        imports: Optional[float] = None,
        budget: Optional[float] = None,
        income: Optional[float] = None,
        expense: Optional[float] = None,
        deficit: Optional[float] = None,
        interest: Optional[float] = None,
        poverty: Optional[float] = None,
        labor: Optional[float] = None,
        migration: Optional[float] = None,
        reverse: Optional[float] = None,
        military_factories: Optional[int] = None,
        factories: Optional[int] = None,
        farms: Optional[int] = None,
        ports: Optional[int] = None,
        centralization_ports: Optional[bool] = None,
        private_business: Optional[bool] = None,
        birth: Optional[float] = None,
        death: Optional[float] = None
    ) -> Economy:
        economy = Economy(
            cid=cid,
            gdp=gdp,
            population=population,
            inflation=inflation,
            capita=capita,
            debt=debt,
            unemployment=unemployment,
            exports=exports,
            imports=imports,
            budget=budget,
            income=income,
            expense=expense,
            deficit=deficit,
            interest=interest,
            poverty=poverty,
            labor=labor,
            migration=migration,
            reverse=reverse,
            military_factories=military_factories,
            factories=factories,
            farms=farms,
            ports=ports,
            centralization_ports=centralization_ports,
            private_business=private_business,
            birth=birth,
            death=death
        )
        self.session.add(economy)
        await self.session.commit()
        await self.session.refresh(economy)
        return economy
    
    async def get_economy(self, cid: int) -> Optional[Economy]:
        result = await self.session.execute(
            select(Economy).where(Economy.cid == cid)
        )
        return result.scalars().first()
    
    async def update(self, **kwargs) -> Optional[Economy]:
        stmt = update(Economy).where(Economy.cid == kwargs['cid']).values(**kwargs).returning(Economy)
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.scalars().first()
    
    async def delete_economy(self, cid: int) -> bool:
        stmt = delete(Economy).where(Economy.cid == cid)
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.rowcount > 0
    
class GroupRequest:
    def __init__(self, session: AsyncSession):
        self.session = session
        
    async def add_group(self, gid: int, name: str, owner: int, admins: list, start_date: Optional[date] = None, current_date: Optional[date] = None, created_at: Optional[date] = None, sid: Optional[int] = None) -> Group:
        group = Group(
            gid=gid,
            name=name,
            owner=owner,
            admins=admins,
            start_date=start_date,
            current_date=current_date,
            created_at=created_at,
            sid=sid
        )
        self.session.add(group)
        await self.session.commit()
        await self.session.refresh(group)
        return group
    
    async def get_group(self, gid: int) -> Optional[Group]:
        result = await self.session.execute(
            select(Group).where(Group.gid == gid)
        )
        return result.scalars().first()
    
    async def update(self, **kwargs) -> Optional[Group]:
        stmt = update(Group).where(Group.gid == kwargs['gid']).values(**kwargs).returning(Group)
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.scalars().first()
    
    async def delete_group(self, gid: int) -> bool:
        stmt = delete(Group).where(Group.gid == gid)
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.rowcount > 0