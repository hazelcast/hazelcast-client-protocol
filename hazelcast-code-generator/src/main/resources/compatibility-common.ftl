<#function convertTypeToSampleValue javaType>
    <#switch javaType?trim>
        <#case "int">
            <#return "anInt">
        <#case "short">
            <#return "aShort">
        <#case "boolean">
            <#return "aBoolean">
        <#case "byte">
            <#return "aByte">
        <#case "long">
            <#return "aLong">
        <#case "char">
            <#return "aChar">
        <#case "long[]">
            <#return "arrLongs">
        <#case util.DATA_FULL_NAME>
            <#return "aData">
        <#case "java.lang.String">
            <#return "aString">
        <#case "java.util.UUID">
            <#return "aUUID">
        <#case "boolean">
            <#return "boolean">
        <#case "java.util.List<" + util.DATA_FULL_NAME + ">">
            <#return "datas">
        <#case "java.util.List<com.hazelcast.core.Member>">
            <#return "members">
        <#case "java.util.List<com.hazelcast.client.impl.client.DistributedObjectInfo>">
            <#return "distributedObjectInfos">
        <#case "java.util.List<java.util.Map.Entry<com.hazelcast.nio.Address,java.util.List<java.lang.Integer>>>">
            <#return "aPartitionTable">
        <#case "java.util.List<java.util.Map.Entry<"+ util.DATA_FULL_NAME + "," + util.DATA_FULL_NAME + ">>">
            <#return "aListOfEntry">
        <#case "java.util.List<java.util.Map.Entry<com.hazelcast.core.Member,java.util.List<com.hazelcast.scheduledexecutor.ScheduledTaskHandler>>>">
            <#return "taskHandlers">
        <#case "com.hazelcast.map.impl.SimpleEntryView<" + util.DATA_FULL_NAME +"," + util.DATA_FULL_NAME +">">
            <#return "anEntryView">
        <#case "java.util.List<java.util.Map.Entry<java.lang.String,java.util.List<java.util.Map.Entry<java.lang.Integer,java.lang.Long>>>>">
            <#return "aNamePartitionSequenceList">
        <#case "java.util.List<java.util.Map.Entry<java.lang.Integer,java.util.UUID>>">
            <#return "aPartitionUuidList">
        <#case "com.hazelcast.nio.Address">
            <#return "anAddress">
        <#case "com.hazelcast.core.Member">
            <#return "aMember">
        <#case "javax.transaction.xa.Xid">
            <#return "anXid">
        <#case "com.hazelcast.map.impl.querycache.event.QueryCacheEventData">
            <#return "aQueryCacheEventData">
        <#case "java.util.List<com.hazelcast.mapreduce.JobPartitionState>">
            <#return "jobPartitionStates">
        <#case "java.util.List<com.hazelcast.map.impl.querycache.event.QueryCacheEventData>">
            <#return "queryCacheEventDatas">
        <#case "java.util.List<com.hazelcast.cache.impl.CacheEventData>">
            <#return "cacheEventDatas">
        <#case "java.util.List<java.lang.String>">
            <#return "strings">
        <#case "java.util.List<java.lang.Long>">
            <#return "longs">
        <#case "java.util.List<java.util.UUID>">
            <#return "uuids">
        <#default>
            <#return "Unknown Data Type " + javaType>
    </#switch>
</#function>
