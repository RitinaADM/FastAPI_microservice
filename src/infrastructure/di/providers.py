from dishka import Provider, Scope, make_async_container, provide
from infrastructure.adapters.outbound.database.mongodb.category_repository_impl import MongoCategoryRepository
from infrastructure.adapters.outbound.message_bus.rabbitmq_publisher import RabbitMQCategoryEventPublisher
from infrastructure.adapters.outbound.cache.redis_adapter import RedisCacheAdapter
from infrastructure.adapters.outbound.cache.cached_category_repository import CachedCategoryRepository
from application.use_cases.category_read_use_case import CategoryReadUseCase
from application.use_cases.category_write_use_case import CategoryWriteUseCase
from application.use_cases.category_statistics_use_case import CategoryStatisticsUseCase
from infrastructure.config.settings import Settings
import pika
from urllib.parse import urlparse


class AdaptersProvider(Provider):
    @provide(scope=Scope.APP)
    def provide_settings(self) -> Settings:
        return Settings()

    @provide(scope=Scope.APP)
    def provide_mongo_category_repository(self, settings: Settings) -> MongoCategoryRepository:
        return MongoCategoryRepository(
            connection_string=settings.mongodb_connection_string,
            database_name=settings.mongodb_database_name
        )

    @provide(scope=Scope.APP)
    def provide_rabbitmq_category_event_publisher(self, settings: Settings) -> RabbitMQCategoryEventPublisher:
        # Parse the URL to extract connection parameters
        parsed_url = urlparse(settings.rabbitmq_url)
        connection_params = pika.ConnectionParameters(
            host=parsed_url.hostname or 'localhost',
            port=parsed_url.port or 5672,
            virtual_host=parsed_url.path or '/',
            credentials=pika.PlainCredentials(
                parsed_url.username or 'guest',
                parsed_url.password or 'guest'
            )
        )
        return RabbitMQCategoryEventPublisher(connection_params, settings.rabbitmq_exchange_name)
    
    @provide(scope=Scope.APP)
    def provide_redis_cache_adapter(self, settings: Settings) -> RedisCacheAdapter:
        return RedisCacheAdapter(settings)


class InteractorProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def provide_category_read_use_case(
        self,
        cached_repository: CachedCategoryRepository
    ) -> CategoryReadUseCase:
        return CategoryReadUseCase(cached_repository)
    
    @provide(scope=Scope.REQUEST)
    def provide_category_write_use_case(
        self,
        cached_repository: CachedCategoryRepository,
        event_publisher: RabbitMQCategoryEventPublisher
    ) -> CategoryWriteUseCase:
        return CategoryWriteUseCase(cached_repository, event_publisher)
    
    @provide(scope=Scope.APP)
    def provide_cached_category_repository(
        self,
        repository: MongoCategoryRepository,
        cache_adapter: RedisCacheAdapter
    ) -> CachedCategoryRepository:
        return CachedCategoryRepository(repository, cache_adapter)
    
    @provide(scope=Scope.REQUEST)
    def provide_category_statistics_use_case(
        self,
        read_use_case: CategoryReadUseCase
    ) -> CategoryStatisticsUseCase:
        return CategoryStatisticsUseCase(read_use_case)


def get_container():
    providers = [
        AdaptersProvider(),
        InteractorProvider()
    ]
    return make_async_container(*providers)