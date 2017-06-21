/*
 * Copyright (c) 2008-2017, Hazelcast, Inc. All Rights Reserved.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

package com.hazelcast.client.impl.protocol.template;

import com.hazelcast.annotation.GenerateCodec;
import com.hazelcast.annotation.Nullable;
import com.hazelcast.annotation.Request;
import com.hazelcast.annotation.Since;
import com.hazelcast.client.impl.protocol.constants.ResponseMessageConst;
import com.hazelcast.client.impl.protocol.task.dynamicconfig.EvictionConfigHolder;
import com.hazelcast.client.impl.protocol.task.dynamicconfig.ListenerConfigHolder;
import com.hazelcast.client.impl.protocol.task.dynamicconfig.MapStoreConfigHolder;
import com.hazelcast.client.impl.protocol.task.dynamicconfig.NearCacheConfigHolder;
import com.hazelcast.client.impl.protocol.task.dynamicconfig.QueryCacheConfigHolder;
import com.hazelcast.client.impl.protocol.task.dynamicconfig.QueueStoreConfigHolder;
import com.hazelcast.client.impl.protocol.task.dynamicconfig.RingbufferStoreConfigHolder;
import com.hazelcast.config.CacheSimpleConfig.ExpiryPolicyFactoryConfig.TimedExpiryPolicyFactoryConfig;
import com.hazelcast.config.CacheSimpleEntryListenerConfig;
import com.hazelcast.config.HotRestartConfig;
import com.hazelcast.config.MapAttributeConfig;
import com.hazelcast.config.MapIndexConfig;
import com.hazelcast.config.WanReplicationRef;
import com.hazelcast.nio.serialization.Data;

import java.util.List;

@GenerateCodec(id = TemplateConstants.DYNAMIC_CONFIG_TEMPLATE_ID, name = "DynamicConfig", ns = "Hazelcast.Client.Protocol.Codec")
@Since("1.5")
public interface DynamicConfigTemplate {

    /**
     * Adds a new multimap config to a running cluster.
     * If a multimap configuration with the given {@code name} already exists, then
     * the new multimap config is ignored and the existing one is preserved.
     *
     * @param name              multimap configuration name
     * @param collectionType    value collection type. Valid values are SET and LIST.
     * @param listenerConfigs   entry listener configurations
     * @param binary            {@code true} to store values in {@code BINARY} format or {@code false} to store
     *                          values in {@code OBJECT} format.
     * @param backupCount       number of synchronous backups
     * @param asyncBackupCount  number of asynchronous backups
     * @param statisticsEnabled set to {@code true} to enable statistics on this multimap configuration
     */
    @Request(id = 1, retryable = false, response = ResponseMessageConst.VOID)
    void addMultiMapConfig(String name, String collectionType, @Nullable List<ListenerConfigHolder> listenerConfigs,
                           boolean binary, int backupCount, int asyncBackupCount, boolean statisticsEnabled);

    /**
     * Adds a new ringbuffer configuration to a running cluster.
     * If a ringbuffer configuration with the given {@code name} already exists, then
     * the new ringbuffer config is ignored and the existing one is preserved.
     *
     * @param name                  ringbuffer configuration name
     * @param capacity              capacity of the ringbuffer
     * @param backupCount           number of synchronous backups
     * @param asyncBackupCount      number of asynchronous backups
     * @param timeToLiveSeconds     maximum number of seconds for each entry to stay in the ringbuffer
     * @param inMemoryFormat        in memory format of items in the ringbuffer. Valid options are {@code BINARY}
     *                              and {@code OBJECT}
     * @param ringbufferStoreConfig backing ringbuffer store configuration
     */
    @Request(id = 2, retryable = false, response = ResponseMessageConst.VOID)
    void addRingbufferConfig(String name, int capacity, int backupCount, int asyncBackupCount, int timeToLiveSeconds,
                             String inMemoryFormat, @Nullable RingbufferStoreConfigHolder ringbufferStoreConfig);

    /**
     * Adds a new cardinality estimator configuration to a running cluster.
     * If a cardinality estimator configuration with the given {@code name} already exists, then
     * the new configuration is ignored and the existing one is preserved.
     *
     * @param name              name of the cardinality estimator configuration
     * @param backupCount       number of synchronous backups
     * @param asyncBackupCount  number of asynchronous backups
     */
    @Request(id = 3, retryable = false, response = ResponseMessageConst.VOID)
    void addCardinalityEstimatorConfig(String name, int backupCount, int asyncBackupCount);

    /**
     * Adds a new lock configuration to a running cluster.
     * If a lock configuration with the given {@code name} already exists, then
     * the new configuration is ignored and the existing one is preserved.
     *
     * @param name       lock's name
     * @param quorumName name of an existing configured quorum to be used to determine the minimum number of members
     *                   required in the cluster for the lock to remain functional. When {@code null}, quorum does not
     *                   apply to this lock configuration's operations.
     */
    @Request(id = 4, retryable = false, response = ResponseMessageConst.VOID)
    void addLockConfig(String name, @Nullable String quorumName);

    /**
     * Adds a new list configuration to a running cluster.
     * If a list configuration with the given {@code name} already exists, then
     * the new configuration is ignored and the existing one is preserved.
     *
     * @param name              list's name
     * @param listenerConfigs   item listener configurations
     * @param backupCount       number of synchronous backups
     * @param asyncBackupCount  number of asynchronous backups
     * @param maxSize           maximum size of the list
     * @param statisticsEnabled {@code true} to enable gathering of statistics on the list, otherwise {@code false}
     */
    @Request(id = 5, retryable = false, response = ResponseMessageConst.VOID)
    void addListConfig(String name, @Nullable List<ListenerConfigHolder> listenerConfigs, int backupCount,
                       int asyncBackupCount, int maxSize, boolean statisticsEnabled);

    /**
     * Adds a new set configuration to a running cluster.
     * If a set configuration with the given {@code name} already exists, then
     * the new configuration is ignored and the existing one is preserved.
     *
     * @param name              set's name
     * @param listenerConfigs   item listener configurations
     * @param backupCount       number of synchronous backups
     * @param asyncBackupCount  number of asynchronous backups
     * @param maxSize           maximum size of the set
     * @param statisticsEnabled {@code true} to enable gathering of statistics on the list, otherwise {@code false}
     */
    @Request(id = 6, retryable = false, response = ResponseMessageConst.VOID)
    void addSetConfig(String name, @Nullable List<ListenerConfigHolder> listenerConfigs, int backupCount,
                       int asyncBackupCount, int maxSize, boolean statisticsEnabled);

    /**
     * Adds a new replicated map configuration to a running cluster.
     * If a replicated map configuration with the given {@code name} already exists, then
     * the new configuration is ignored and the existing one is preserved.
     *
     * @param name              name of the replicated map configuration
     * @param inMemoryFormat    data type used to store entries. Valid values are {@code "BINARY"}, {@code "OBJECT"}
     *                          and {@code "NATIVE"}.
     * @param asyncFillup       {@code true} to make the replicated map available for reads before initial replication
     *                          is completed, {@code false} otherwise.
     * @param statisticsEnabled {@code true} to enable gathering of statistics, otherwise {@code false}
     * @param mergePolicy       class name of a class implementing
     *                          {@code com.hazelcast.replicatedmap.merge.ReplicatedMapMergePolicy} to merge entries
     *                          while recovering from a split brain
     * @param listenerConfigs   entry listener configurations
     */
    @Request(id = 7, retryable = false, response = ResponseMessageConst.VOID)
    void addReplicatedMapConfig(String name, String inMemoryFormat, boolean asyncFillup, boolean statisticsEnabled,
                                String mergePolicy, @Nullable List<ListenerConfigHolder> listenerConfigs);

    /**
     * Adds a new topic configuration to a running cluster.
     * If a topic configuration with the given {@code name} already exists, then
     * the new configuration is ignored and the existing one is preserved.
     *
     * @param name                  topic's name
     * @param globalOrderingEnabled when {@code true} all nodes listening to the same topic get their messages in
     *                              the same order
     * @param statisticsEnabled     {@code true} to enable gathering of statistics, otherwise {@code false}
     * @param multiThreadingEnabled {@code true} to enable multi-threaded processing of incoming messages, otherwise
     *                              a single thread will handle all topic messages
     * @param listenerConfigs       message listener configurations
     */
    @Request(id = 8, retryable = false, response = ResponseMessageConst.VOID)
    void addTopicConfig(String name, boolean globalOrderingEnabled, boolean statisticsEnabled,
                        boolean multiThreadingEnabled, @Nullable List<ListenerConfigHolder> listenerConfigs);

    /**
     * Adds a new executor configuration to a running cluster.
     * If an executor configuration with the given {@code name} already exists, then
     * the new configuration is ignored and the existing one is preserved.
     *
     * @param name              executor's name
     * @param poolSize          executor thread pool size
     * @param queueCapacity     capacity of executor queue. A value of {@code 0} implies {@link Integer#MAX_VALUE}
     * @param statisticsEnabled {@code true} to enable gathering of statistics, otherwise {@code false}
     */
    @Request(id = 9, retryable = false, response = ResponseMessageConst.VOID)
    void addExecutorConfig(String name, int poolSize, int queueCapacity, boolean statisticsEnabled);

    /**
     * Adds a new durable executor configuration to a running cluster.
     * If a durable executor configuration with the given {@code name} already exists, then
     * the new configuration is ignored and the existing one is preserved.
     *
     * @param name          durable executor name
     * @param poolSize      executor thread pool size
     * @param durability    executor's durability
     * @param capacity      capacity of executor tasks per partition
     */
    @Request(id = 10, retryable = false, response = ResponseMessageConst.VOID)
    void addDurableExecutorConfig(String name, int poolSize, int durability, int capacity);

    /**
     * Adds a new scheduled executor configuration to a running cluster.
     * If a scheduled executor configuration with the given {@code name} already exists, then
     * the new configuration is ignored and the existing one is preserved.
     *
     * @param name       name of scheduled executor
     * @param poolSize   number of executor threads per member for the executor
     * @param durability durability of the scheduled executor
     * @param capacity   maximum number of tasks that a scheduler can have at any given point in time per partition
     */
    @Request(id = 11, retryable = false, response = ResponseMessageConst.VOID)
    void addScheduledExecutorConfig(String name, int poolSize, int durability, int capacity);

    /**
     * Adds a new semaphore configuration to a running cluster.
     * If a semaphore configuration with the given {@code name} already exists, then
     * the new configuration is ignored and the existing one is preserved.
     *
     * @param name              semaphore configuration name
     * @param initialPermits    thread count to which the concurrent access is limited
     * @param backupCount       number of synchronous backups
     * @param asyncBackupCount  number of asynchronous backups
     */
    @Request(id = 12, retryable = false, response = ResponseMessageConst.VOID)
    void addSemaphoreConfig(String name, int initialPermits, int backupCount, int asyncBackupCount);

    /**
     * Adds a new queue configuration to a running cluster.
     * If a queue configuration with the given {@code name} already exists, then
     * the new configuration is ignored and the existing one is preserved.
     *
     * @param name              queue name
     * @param listenerConfigs   item listeners configuration
     * @param backupCount       number of synchronous backups
     * @param asyncBackupCount  number of asynchronous backups
     * @param maxSize           maximum number of items in the queue
     * @param emptyQueueTtl     queue time-to-live in seconds: queue will be destroyed if it stays empty or unused for that time
     * @param statisticsEnabled {@code true} to enable gathering of statistics, otherwise {@code false}
     * @param quorumName        name of an existing configured quorum to be used to determine the minimum number of members
     *                          required in the cluster for the queue to remain functional. When {@code null}, quorum does not
     *                          apply to this queue configuration's operations.
     * @param queueStoreConfig  backing queue store configuration
     */
    @Request(id = 13, retryable = false, response = ResponseMessageConst.VOID)
    void addQueueConfig(String name, @Nullable List<ListenerConfigHolder> listenerConfigs, int backupCount,
                        int asyncBackupCount, int maxSize, int emptyQueueTtl, boolean statisticsEnabled,
                        @Nullable String quorumName, @Nullable QueueStoreConfigHolder queueStoreConfig);

    /**
     * Adds a new map configuration to a running cluster.
     * If a map configuration with the given {@code name} already exists, then
     * the new configuration is ignored and the existing one is preserved.
     *
     * @param name
     * @param backupCount                           number of synchronous backups
     * @param asyncBackupCount                      number of asynchronous backups
     * @param timeToLiveSeconds                     maximum number of seconds for each entry to stay in the map.
     * @param maxIdleSeconds                        maximum number of seconds for each entry to stay idle in the map
     * @param evictionPolicy                        eviction policy. Valid values: {@code NONE} (no eviction), {@code LRU}
     *                                              (Least Recently Used), {@code LFU} (Least Frequently Used),
     *                                              {@code RANDOM} (evict random entry).
     * @param readBackupData                        {@code true} to enable reading local backup entries, {@code false} otherwise
     * @param cacheDeserializedValues               control caching of de-serialized values. Valid values are {@code NEVER}
     *                                              (Never cache de-serialized object), {@code INDEX_ONLY} (Cache values only
     *                                              when they are inserted into an index) and {@code ALWAYS} (Always cache
     *                                              de-serialized values
     * @param mergePolicy                           class name of a class implementing
     *                                              {@code com.hazelcast.map.merge.MapMergePolicy} to merge entries
     *                                              while recovering from a split brain
     * @param inMemoryFormat                        data type used to store entries. Valid values are {@code BINARY},
     *                                              {@code OBJECT} and {@code NATIVE}.
     * @param listenerConfigs                       entry listener configurations
     * @param partitionLostListenerConfigs          partition lost listener configurations
     * @param statisticsEnabled                     {@code true} to enable gathering of statistics, otherwise {@code false}
     * @param quorumName                            name of an existing configured quorum to be used to determine the minimum
     *                                              number of members required in the cluster for the map to remain functional.
     *                                              When {@code null}, quorum does not apply to this map's operations.
     * @param mapEvictionPolicy                     custom {@code com.hazelcast.map.eviction.MapEvictionPolicy} implementation
     *                                              or {@code null}
     * @param maxSizeConfigMaxSizePolicy            maximum size policy. Valid values are {@code PER_NODE},
     *                                              {@code PER_PARTITION}, {@code USED_HEAP_PERCENTAGE}, {@code USED_HEAP_SIZE},
     *                                              {@code FREE_HEAP_PERCENTAGE}, {@code FREE_HEAP_SIZE},
     *                                              {@code USED_NATIVE_MEMORY_SIZE}, {@code USED_NATIVE_MEMORY_PERCENTAGE},
     *                                              {@code FREE_NATIVE_MEMORY_SIZE}, {@code FREE_NATIVE_MEMORY_PERCENTAGE}.
     * @param maxSizeConfigSize                     maximum size of map
     * @param mapStoreConfig                        configuration of backing map store or {@code null} for none
     * @param nearCacheConfig                       configuration of near cache or {@code null} for none
     * @param wanReplicationRef                     reference to an existing WAN replication configuration
     * @param mapIndexConfigs                       map index configurations
     * @param mapAttributeConfigs                   map attributes
     * @param queryCacheConfigs                     configurations for query caches on this map
     * @param partitioningStrategyClassName         name of class implementing {@code com.hazelcast.core.PartitioningStrategy}
     *                                              or {@code null}
     * @param partitioningStrategyImplementation    a serialized instance of a partitioning strategy
     * @param hotRestartConfig                      hot restart configuration
     */
    @Request(id = 14, retryable = false, response = ResponseMessageConst.VOID)
    void addMapConfig(String name, int backupCount, int asyncBackupCount, int timeToLiveSeconds, int maxIdleSeconds,
                      String evictionPolicy, boolean readBackupData, String cacheDeserializedValues, String mergePolicy,
                      String inMemoryFormat, @Nullable List<ListenerConfigHolder> listenerConfigs,
                      @Nullable List<ListenerConfigHolder> partitionLostListenerConfigs, boolean statisticsEnabled,
                      @Nullable String quorumName, @Nullable Data mapEvictionPolicy,
                      String maxSizeConfigMaxSizePolicy, int maxSizeConfigSize,
                      @Nullable MapStoreConfigHolder mapStoreConfig,
                      @Nullable NearCacheConfigHolder nearCacheConfig,
                      @Nullable WanReplicationRef wanReplicationRef,
                      @Nullable List<MapIndexConfig> mapIndexConfigs,
                      @Nullable List<MapAttributeConfig> mapAttributeConfigs,
                      @Nullable List<QueryCacheConfigHolder> queryCacheConfigs,
                      @Nullable String partitioningStrategyClassName,
                      @Nullable Data partitioningStrategyImplementation,
                      @Nullable HotRestartConfig hotRestartConfig);

    /**
     * Adds a new reliable topic configuration to a running cluster.
     * If a reliable topic configuration with the given {@code name} already exists, then
     * the new configuration is ignored and the existing one is preserved.
     *
     * @param name                  name of reliable topic
     * @param listenerConfigs       message listener configurations
     * @param readBatchSize         maximum number of items to read in a batch.
     * @param statisticsEnabled     {@code true} to enable gathering of statistics, otherwise {@code false}
     * @param topicOverloadPolicy   policy to handle an overloaded topic. Available values are {@code DISCARD_OLDEST},
     *                              {@code DISCARD_NEWEST}, {@code BLOCK} and {@code ERROR}.
     * @param executor              a serialized {@link java.util.concurrent.Executor} instance to use for executing
     *                              message listeners or {@code null}
     */
    @Request(id = 15, retryable = false, response = ResponseMessageConst.VOID)
    void addReliableTopicConfig(String name, @Nullable List<ListenerConfigHolder> listenerConfigs, int readBatchSize,
                                boolean statisticsEnabled, String topicOverloadPolicy, @Nullable Data executor);

    /**
     * Adds a new cache configuration to a running cluster.
     * If a cache configuration with the given {@code name} already exists, then
     * the new configuration is ignored and the existing one is preserved.
     *
     * @param name                                  cache name
     * @param keyType                               class name of key type
     * @param valueType                             class name of value type
     * @param statisticsEnabled                     {@code true} to enable gathering of statistics, otherwise {@code false}
     * @param managementEnabled                     {@code true} to enable management interface on this cache or {@code false}
     * @param readThrough                           {@code true} to enable read through from a {@code CacheLoader}
     * @param writeThrough                          {@code true} to enable write through to a {@code CacheWriter}
     * @param cacheLoaderFactory                    name of cache loader factory class, if one is configured
     * @param cacheWriterFactory                    name of cache writer factory class, if one is configured
     * @param cacheLoader                           name of cache loader implementation class
     * @param cacheWriter                           name of cache writer implementation class
     * @param backupCount                           number of synchronous backups
     * @param asyncBackupCount                      number of asynchronous backups
     * @param inMemoryFormat                        data type used to store entries. Valid values are {@code BINARY},
     *                                              {@code OBJECT} and {@code NATIVE}.
     * @param quorumName                            name of an existing configured quorum to be used to determine the minimum
     *                                              number of members required in the cluster for the cache to remain functional.
     *                                              When {@code null}, quorum does not apply to this cache's operations.
     * @param mergePolicy                           name of a class implementing {@link com.hazelcast.cache.CacheMergePolicy}
     *                                              that handles merging of values for this cache while recovering from
     *                                              network partitioning
     * @param disablePerEntryInvalidationEvents     when {@code true} disables invalidation events for per entry but
     *                                              full-flush invalidation events are still enabled.
     * @param partitionLostListenerConfigs          partition lost listener configurations
     * @param expiryPolicyFactoryClassName          expiry policy factory class name. When configuring an expiry policy,
     *                                              either this or {@ode timedExpiryPolicyFactoryConfig} should be configured.
     * @param timedExpiryPolicyFactoryConfig        expiry policy factory with duration configuration
     * @param cacheEntryListeners                   cache entry listeners configuration
     * @param evictionConfig                        cache eviction configuration
     * @param wanReplicationRef                     reference to an existing WAN replication configuration
     * @param hotRestartConfig                      hot restart configuration
     */
    @Request(id = 16, retryable = false, response = ResponseMessageConst.VOID)
    void addCacheConfig(String name, @Nullable String keyType, @Nullable String valueType, boolean statisticsEnabled,
                        boolean managementEnabled, boolean readThrough, boolean writeThrough,
                        @Nullable String cacheLoaderFactory, @Nullable String cacheWriterFactory, @Nullable String cacheLoader,
                        @Nullable String cacheWriter, int backupCount, int asyncBackupCount, String inMemoryFormat,
                        @Nullable String quorumName, @Nullable String mergePolicy,
                        boolean disablePerEntryInvalidationEvents,
                        @Nullable List<ListenerConfigHolder> partitionLostListenerConfigs,
                        @Nullable String expiryPolicyFactoryClassName,
                        @Nullable TimedExpiryPolicyFactoryConfig timedExpiryPolicyFactoryConfig,
                        @Nullable List<CacheSimpleEntryListenerConfig> cacheEntryListeners,
                        @Nullable EvictionConfigHolder evictionConfig,
                        @Nullable WanReplicationRef wanReplicationRef,
                        @Nullable HotRestartConfig hotRestartConfig);

}
