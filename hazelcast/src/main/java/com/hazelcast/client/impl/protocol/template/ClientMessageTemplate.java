/*
 * Copyright (c) 2008-2018, Hazelcast, Inc. All Rights Reserved.
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
import com.hazelcast.client.impl.protocol.constants.EventMessageConst;
import com.hazelcast.client.impl.protocol.constants.ResponseMessageConst;
import com.hazelcast.nio.Address;
import com.hazelcast.nio.serialization.Data;

import java.util.List;
import java.util.Map;

@GenerateCodec(id = TemplateConstants.CLIENT_TEMPLATE_ID, name = "Client", ns = "Hazelcast.Client.Protocol.Codec")
public interface ClientMessageTemplate {

    /**
     * @param username             Name of the user for authentication.
     * @param password             Password for the user.
     * @param uuid                 Unique string identifying the connected client uniquely. This string is generated by the owner member server
     *                             on initial connection. When the client connects to a non-owner member it sets this field on the request.
     * @param ownerUuid            Unique string identifying the server member uniquely.
     * @param isOwnerConnection    You must set this field to true while connecting to the owner member, otherwise set to false.
     * @param clientType           The type of the client. E.g. JAVA, CPP, CSHARP, etc.
     * @param serializationVersion client side supported version to inform server side
     * @param clientHazelcastVersion The Hazelcast version of the client. (e.g. 3.7.2)
     * @return Returns the address, uuid and owner uuid.
     */
    @Request(id = 2, retryable = true, response = ResponseMessageConst.AUTHENTICATION)
    Object authentication(String username, String password, @Nullable String uuid, @Nullable String ownerUuid,
                          boolean isOwnerConnection, String clientType, byte serializationVersion,
                          @Since (value = "1.3") String clientHazelcastVersion);

    /**
     * @param credentials          Secret byte array for authentication.
     * @param uuid                 Unique string identifying the connected client uniquely. This string is generated by the owner member server
     *                             on initial connection. When the client connects to a non-owner member it sets this field on the request.
     * @param ownerUuid            Unique string identifying the server member uniquely.
     * @param isOwnerConnection    You must set this field to true while connecting to the owner member, otherwise set to false.
     * @param clientType           The type of the client. E.g. JAVA, CPP, CSHARP, etc.
     * @param serializationVersion client side supported version to inform server side
     * @param clientHazelcastVersion The Hazelcast version of the client. (e.g. 3.7.2)
     * @return Returns the address, uuid and owner uuid.
     */

    @Request(id = 3, retryable = true, response = ResponseMessageConst.AUTHENTICATION)
    Object authenticationCustom(Data credentials, @Nullable String uuid, @Nullable String ownerUuid, boolean isOwnerConnection,
                                String clientType, byte serializationVersion,
                                @Since (value = "1.3") String clientHazelcastVersion);

    /**
     * @param localOnly if true only master node sends events, otherwise all registered nodes send all membership
     *                  changes.
     * @return Returns the registration id for the listener.
     */
    @Request(id = 4, retryable = false, response = ResponseMessageConst.STRING,
            event = {EventMessageConst.EVENT_MEMBER, EventMessageConst.EVENT_MEMBERLIST, EventMessageConst.EVENT_MEMBERATTRIBUTECHANGE})
    Object addMembershipListener(boolean localOnly);

    /**
     * @param name        The distributed object name for which the proxy is being created for.
     * @param serviceName The name of the service. Possible service names are:
     *                    "hz:impl:listService"
     *                    "hz:impl:queueService"
     *                    "hz:impl:setService"
     *                    "hz:impl:atomicLongService"
     *                    "hz:impl:atomicReferenceService"
     *                    "hz:impl:countDownLatchService"
     *                    "hz:impl:idGeneratorService"
     *                    "hz:impl:semaphoreService"
     *                    "hz:impl:executorService"
     *                    "hz:impl:mapService"
     *                    "hz:impl:mapReduceService"
     *                    "hz:impl:multiMapService"
     *                    "hz:impl:quorumService"
     *                    "hz:impl:replicatedMapService"
     *                    "hz:impl:ringbufferService"
     *                    "hz:core:proxyService"
     *                    "hz:impl:reliableTopicService"
     *                    "hz:impl:topicService"
     *                    "hz:core:txManagerService"
     *                    "hz:impl:xaService"
     */
    @Request(id = 5, retryable = false, response = ResponseMessageConst.VOID)
    void createProxy(String name, String serviceName, Address target);

    /**
     * @param name        The distributed object name for which the proxy is being destroyed for.
     * @param serviceName The name of the service. Possible service names are:
     *                    "hz:impl:listService"
     *                    "hz:impl:queueService"
     *                    "hz:impl:setService"
     *                    "hz:impl:atomicLongService"
     *                    "hz:impl:atomicReferenceService"
     *                    "hz:impl:countDownLatchService"
     *                    "hz:impl:idGeneratorService"
     *                    "hz:impl:semaphoreService"
     *                    "hz:impl:executorService"
     *                    "hz:impl:mapService"
     *                    "hz:impl:mapReduceService"
     *                    "hz:impl:multiMapService"
     *                    "hz:impl:quorumService"
     *                    "hz:impl:replicatedMapService"
     *                    "hz:impl:ringbufferService"
     *                    "hz:core:proxyService"
     *                    "hz:impl:reliableTopicService"
     *                    "hz:impl:topicService"
     *                    "hz:core:txManagerService"
     *                    "hz:impl:xaService"
     */

    @Request(id = 6, retryable = false, response = ResponseMessageConst.VOID)
    void destroyProxy(String name, String serviceName);

    /**
     * @return The partition list for each member address.
     */
    @Request(id = 8, retryable = false, response = ResponseMessageConst.PARTITIONS)
    Object getPartitions();

    @Request(id = 9, retryable = false, response = ResponseMessageConst.VOID)
    void removeAllListeners();

    /**
     * @param localOnly if true only node that has the partition sends the request, if false
     *                  sends all partition lost events.
     * @return The listener registration id.
     */
    @Request(id = 10, retryable = false, response = ResponseMessageConst.STRING, event = {EventMessageConst.EVENT_PARTITIONLOST})
    Object addPartitionLostListener(boolean localOnly);

    /**
     * @param registrationId The id assigned during the listener registration.
     * @return true if the listener existed and removed, false otherwise.
     */
    @Request(id = 11, retryable = true, response = ResponseMessageConst.BOOLEAN)
    Object removePartitionLostListener(String registrationId);

    /**
     * @return An array of distributed object info in the cluster.
     */
    @Request(id = 12, retryable = false, response = ResponseMessageConst.LIST_DISTRIBUTED_OBJECT)
    Object getDistributedObjects();

    /**
     * @param localOnly If set to true, the server adds the listener only to itself, otherwise the listener is is added for all
     *                  members in the cluster.
     * @return The registration id for the distributed object listener.
     */
    @Request(id = 13, retryable = false, response = ResponseMessageConst.STRING, event = {EventMessageConst.EVENT_DISTRIBUTEDOBJECT})
    Object addDistributedObjectListener(boolean localOnly);

    /**
     * @param registrationId The id assigned during the registration.
     * @return true if the listener existed and removed, false otherwise.
     */
    @Request(id = 14, retryable = true, response = ResponseMessageConst.BOOLEAN)
    Object removeDistributedObjectListener(String registrationId);

    @Request(id = 15, retryable = true, response = ResponseMessageConst.VOID)
    void ping();

    /**
     * The statistics is a String that is composed of key=value pairs separated by ',' . The following characters
     * ('=' '.' ',' '\') should be escaped in IMap and ICache names by the escape character ('\'). E.g. if the map name is
     * MyMap.First, it will be escaped as: MyMap\.First
     *
     * The statistics key identify the category and name of the statistics. It is formatted as:
     * mainCategory.subCategory.statisticName
     *
     * An e.g. Operating system committedVirtualMemorySize path would be: os.committedVirtualMemorySize
     *
     * Please note that if any client implementation can not provide the value for a statistics, the corresponding key, valaue
     * pair will not be presented in the statistics string. Only the ones, that the client can provide will be added.
     *
     * The statistics key names can be one of the following (Used IMap named <StatIMapName> and ICache Named
     * <StatICacheName> and assuming that the near cache is configured):
     *
     * clientType: The string that represents the client type. See {@link com.hazelcast.core.ClientType}
     *
     * clusterConnectionTimestamp: The time that the client connected to the cluster (milliseconds since epoch). It is reset on
     * each reconnection.
     *
     * credentials.principal: The principal of the client if it exists. For
     * {@link com.hazelcast.security.UsernamePasswordCredentials}, this is the username, for custom authentication it is set by
     * the {@link com.hazelcast.security.Credentials} implementer.
     *
     * clientAddress: The address of the client. It is formatted as "<IP>:<port>"
     *
     * clientName: The name of the client instance. See ClientConfig.setInstanceName.
     *
     * enterprise: "true" if the client is an enterprise client, "false" otherwise.
     *
     * lastStatisticsCollectionTime: The time stamp (milliseconds since epoch) when the latest update for the statistics is
     * collected.
     *
     * Near cache statistics (see {@link com.hazelcast.monitor.NearCacheStats}):
     *
     * nc.<StatIMapName>.creationTime: The creation time (milliseconds since epoch) of this Near Cache on the client.
     *
     * nc.<StatIMapName>.evictions: The number of evictions of Near Cache entries owned by this client.
     *
     * nc.<StatIMapName>.expirations: The number of TTL and max-idle expirations of Near Cache entries owned by the client.
     *
     * nc.<StatIMapName>.hits: The number of hits (reads) of Near Cache entries owned by the client.
     *
     * nc.<StatIMapName>.lastPersistenceDuration: The duration in milliseconds of the last Near Cache key persistence
     * (when the pre-load feature is enabled).
     *
     * nc.<StatIMapName>.lastPersistenceFailure: The failure reason of the last Near Cache persistence (when the pre-load
     * feature is enabled).
     *
     * nc.<StatIMapName>.lastPersistenceKeyCount: The number of Near Cache key persistences (when the pre-load feature is
     * enabled).
     *
     * nc.<StatIMapName>.lastPersistenceTime: The timestamp (milliseconds since epoch) of the last Near Cache key
     * persistence (when the pre-load feature is enabled).
     *
     * nc.<StatIMapName>.lastPersistenceWrittenBytes: The written number of bytes of the last Near Cache key persistence
     * (when the pre-load feature is enabled).
     *
     * nc.<StatIMapName>.misses: The number of misses of Near Cache entries owned by the client.
     *
     * nc.<StatIMapName>.ownedEntryCount: the number of Near Cache entries owned by the client.
     *
     * nc.<StatIMapName>.ownedEntryMemoryCost: Memory cost (number of bytes) of Near Cache entries owned by the client.
     *
     * nc.hz/<StatICacheName>.creationTime: The creation time of this Near Cache on the client.
     *
     * nc.hz/<StatICacheName>.evictions: The number of evictions of Near Cache entries owned by the client.
     *
     * nc.hz/<StatICacheName>.expirations: The number of TTL and max-idle expirations of Near Cache entries owned by the
     * client.
     *
     * nc.hz/<StatICacheName>.hits
     * nc.hz/<StatICacheName>.lastPersistenceDuration
     * nc.hz/<StatICacheName>.lastPersistenceFailure
     * nc.hz/<StatICacheName>.lastPersistenceKeyCount
     * nc.hz/<StatICacheName>.lastPersistenceTime
     * nc.hz/<StatICacheName>.lastPersistenceWrittenBytes
     * nc.hz/<StatICacheName>.misses
     * nc.hz/<StatICacheName>.ownedEntryCount
     * nc.hz/<StatICacheName>.ownedEntryMemoryCost
     *
     * Operating System Statistics (see {@link com.hazelcast.internal.metrics.metricsets.OperatingSystemMetricSet},
     * {@link sun.management.OperatingSystemImpl}) and {@link com.sun.management.UnixOperatingSystemMXBean}:
     *
     * os.committedVirtualMemorySize: The amount of virtual memory that is guaranteed to be available to the running process in
     * bytes, or -1 if this operation is not supported.
     *
     * os.freePhysicalMemorySize: The amount of free physical memory in bytes.
     *
     * os.freeSwapSpaceSize: The amount of free swap space in bytes.
     *
     * os.maxFileDescriptorCount: The maximum number of file descriptors.
     *
     * os.openFileDescriptorCount: The number of open file descriptors.
     *
     * os.processCpuTime: The CPU time used by the process in nanoseconds.
     *
     * os.systemLoadAverage: The system load average for the last minute. (See
     * {@link java.lang.management.OperatingSystemMXBean#getSystemLoadAverage})
     * The system load average is the sum of the number of runnable entities
     * queued to the {@link java.lang.management.OperatingSystemMXBean#getAvailableProcessors} available processors
     * and the number of runnable entities running on the available processors
     * averaged over a period of time.
     * The way in which the load average is calculated is operating system
     * specific but is typically a damped time-dependent average.
     * <p>
     * If the load average is not available, a negative value is returned.
     * <p>
     *
     * os.totalPhysicalMemorySize: The total amount of physical memory in bytes.
     *
     * os.totalSwapSpaceSize: The total amount of swap space in bytes.
     *
     * Runtime statistics (See {@link Runtime}:
     *
     * runtime.availableProcessors: The number of processors available to the process.
     *
     * runtime.freeMemory: an approximation to the total amount of memory currently available for future allocated objects,
     * measured in bytes.
     *
     * runtime.maxMemory: The maximum amount of memory that the process will  attempt to use, measured in bytes
     *
     * runtime.totalMemory: The total amount of memory currently available for current and future objects, measured in bytes.
     *
     * runtime.uptime: The uptime of the process in milliseconds.
     *
     * runtime.usedMemory: The difference of total memory and used memory in bytes.
     *
     * userExecutor.queueSize: The number of waiting tasks in the client user executor (See ClientExecutionService#getUserExecutor)
     *
     * Not: Please observe that the name for the ICache appears to be the hazelcast instance name "hz" followed by "/" and
     * followed by the cache name provided which is StatICacheName.
     *
     * An example stats string (IMap name: StatIMapName and ICache name: StatICacheName with near-cache enabled):
     *
     * lastStatisticsCollectionTime=1496137027173,enterprise=false,clientType=JAVA,clusterConnectionTimestamp=1496137018114,
     * clientAddress=127.0.0.1:5001,clientName=hz.client_0,executionService.userExecutorQueueSize=0,runtime.maxMemory=1065025536,
     * os.freePhysicalMemorySize=32067584,os.totalPhysicalMemorySize=17179869184,os.systemLoadAverage=249,
     * runtime.usedMemory=16235040,runtime.freeMemory=115820000,os.totalSwapSpaceSize=5368709120,runtime.availableProcessors=4,
     * runtime.uptime=13616,os.committedVirtualMemorySize=4081422336,os.maxFileDescriptorCount=10240,
     * runtime.totalMemory=132055040,os.processCpuTime=6270000000,os.openFileDescriptorCount=67,os.freeSwapSpaceSize=888406016,
     * nc.StatIMapName.creationTime=1496137021761,nc.StatIMapName.evictions=0,nc.StatIMapName.hits=1,
     * nc.StatIMapName.lastPersistenceDuration=0,nc.StatIMapName.lastPersistenceKeyCount=0,nc.StatIMapName.lastPersistenceTime=0,
     * nc.StatIMapName.lastPersistenceWrittenBytes=0,nc.StatIMapName.misses=1,nc.StatIMapName.ownedEntryCount=1,
     * nc.StatIMapName.expirations=0,nc.StatIMapName.ownedEntryMemoryCost=140,nc.hz/StatICacheName.creationTime=1496137025201,
     * nc.hz/StatICacheName.evictions=0,nc.hz/StatICacheName.hits=1,nc.hz/StatICacheName.lastPersistenceDuration=0,
     * nc.hz/StatICacheName.lastPersistenceKeyCount=0,nc.hz/StatICacheName.lastPersistenceTime=0,
     * nc.hz/StatICacheName.lastPersistenceWrittenBytes=0,nc.hz/StatICacheName.misses=1,nc.hz/StatICacheName.ownedEntryCount=1,
     * nc.hz/StatICacheName.expirations=0,nc.hz/StatICacheName.ownedEntryMemoryCost=140
     *
     *
     * @param stats The key=value pairs separated by the ',' character
     */
    @Request(id = 16, retryable = false, response = ResponseMessageConst.VOID)
    @Since(value = "1.5")
    void statistics(String stats);

    /**
     * Deploys the list of classes to cluster
     * Each item is a Map.Entry<String, byte[]> in the list.
     * key of entry is full class name, and byte[] is the class definition.
     *
     * @param classDefinitions list of class definitions
     */
    @Request(id = 17, retryable = false, response = ResponseMessageConst.VOID)
    @Since(value = "1.5")
    void deployClasses(List<Map.Entry<String, byte[]>> classDefinitions);

    /**
     * Adds partition listener to send server.
     * listener is removed automatically when client disconnected.
     * There is no corresponding removeListener message.
     */
    @Request(id = 18, retryable = false, response = ResponseMessageConst.VOID, event = {EventMessageConst.EVENT_PARTITIONS})
    @Since(value = "1.5")
    void addPartitionListener();

    /**
     * Proxies will be created on all cluster members.
     * If the member is  a lite member, a replicated map will not be created.
     * Any proxy creation failure is logged on the server side.
     * Exceptions related to a proxy creation failure is not send to the client.
     * A proxy creation failure does not cancel this operation, all proxies will be attempted to be created.
     *
     * @param proxies proxies that will be created
     *                Each entry's key is distributed object name.
     *                Each entry's value is service name.
     *                For possible service names see createProxy message.
     */
    @Since(value = "1.6")
    @Request(id = 19, retryable = false, response = ResponseMessageConst.VOID)
    void createProxies(List<Map.Entry<String, String>> proxies);

    /**
     * Collects a metrics data package from the target {@code member}. Packets are
     * streamed from the member to the calling process by frequently calling this
     * method.
     *
     * @param member the {@link Address} of the member that should return its
     *        metrics data
     * @param packageNo what the caller believes the current package sequence number
     *        to be
     * @param memorizedSize the table remembered by the caller (expect
     *        0-memorizedSize-1 as known constants)
     * @param poolSize the current table size of the caller that must not be
     *        exceeded by any of the referenced constants
     * @return the metrics series data as binary data package
     */
    @Since(value = "1.6")
    @Request(id = 20, retryable = false, response = ResponseMessageConst.DATA)
    Object collectMetrics(Address member, long packageNo, int memorizedSize, int poolSize);
}
