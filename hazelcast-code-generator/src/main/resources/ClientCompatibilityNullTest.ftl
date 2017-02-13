<#assign testForVersionString=util.versionAsString(testForVersion)/>
<#assign testForVersionClassName=util.versionAsClassName(testForVersion)/>
package com.hazelcast.client.protocol.compatibility;

import com.hazelcast.cache.impl.CacheEventData;
import com.hazelcast.cache.impl.CacheEventDataImpl;
import com.hazelcast.cache.impl.CacheEventType;
import com.hazelcast.client.impl.MemberImpl;
import com.hazelcast.client.impl.client.DistributedObjectInfo;
import com.hazelcast.client.impl.protocol.ClientMessage;
import com.hazelcast.client.impl.protocol.codec.*;
import com.hazelcast.client.impl.protocol.util.SafeBuffer;
import com.hazelcast.core.Member;
import com.hazelcast.internal.serialization.impl.HeapData;
import com.hazelcast.map.impl.SimpleEntryView;
import com.hazelcast.map.impl.querycache.event.DefaultQueryCacheEventData;
import com.hazelcast.map.impl.querycache.event.QueryCacheEventData;
import com.hazelcast.mapreduce.JobPartitionState;
import com.hazelcast.mapreduce.impl.task.JobPartitionStateImpl;
import com.hazelcast.nio.Address;
import com.hazelcast.scheduledexecutor.ScheduledTaskHandler;
import com.hazelcast.nio.serialization.Data;
import com.hazelcast.transaction.impl.xa.SerializableXID;
import java.io.IOException;
import com.hazelcast.test.HazelcastParallelClassRunner;
import com.hazelcast.test.annotation.ParallelTest;
import com.hazelcast.test.annotation.QuickTest;
import org.junit.experimental.categories.Category;
import org.junit.runner.RunWith;

import java.util.Arrays;
import java.io.IOException;
import java.io.DataInputStream;
import java.io.InputStream;
import java.lang.reflect.Array;
import java.net.UnknownHostException;
import javax.transaction.xa.Xid;
import java.util.AbstractMap;
import java.util.Collection;
import java.util.Collections;
import java.util.HashMap;
import java.util.LinkedList;
import java.util.List;
import java.util.ListIterator;
import java.util.Map;

import static org.junit.Assert.assertTrue;
import static org.junit.Assert.assertFalse;
import static com.hazelcast.client.protocol.compatibility.ReferenceObjects.*;

@RunWith(HazelcastParallelClassRunner.class)
@Category({QuickTest.class, ParallelTest.class})
public class ClientCompatibilityNullTest_${testForVersionClassName} {
    private static final int FRAME_LEN_FIELD_SIZE = 4;

    @org.junit.Test
            public void test() throws IOException {
            InputStream input = getClass().getResourceAsStream("/${testForVersionString}.protocol.compatibility.null.binary");
            DataInputStream inputStream = new DataInputStream(input);
<#list model?keys as key>
<#assign map=model?values[key_index]?values/>
<#if map?has_content>
<#list map as cm>

<#if cm.messageSinceInt lte testForVersion >
{
    ClientMessage clientMessage = ${cm.className}.encodeRequest( <#if cm.requestParams?has_content> <#list cm.requestParams as param>  <#if param.nullable>null<#else>${convertTypeToSampleValue(param.type)}</#if> <#if param_has_next>, </#if> </#list> </#if>);
    int length = inputStream.readInt();
<#if cm.highestParameterVersion lte testForVersion >
    byte[] bytes = new byte[length];
    inputStream.read(bytes);
    assertTrue(isEqual(Arrays.copyOf(clientMessage.buffer().byteArray(), clientMessage.getFrameLength()), bytes));
<#else>
    // Since the test is generated for protocol version (${testForVersionString}) which is earlier than latest change in the message
    // (version ${util.versionAsString(cm.highestParameterVersion)}), only the bytes after frame length fields are compared
    int frameLength = clientMessage.getFrameLength();
    assertTrue(frameLength >= length);
    inputStream.skipBytes(FRAME_LEN_FIELD_SIZE);
    byte[] bytes = new byte[length - FRAME_LEN_FIELD_SIZE];
    inputStream.read(bytes);
    assertTrue(isEqual(Arrays.copyOfRange(clientMessage.buffer().byteArray(), FRAME_LEN_FIELD_SIZE, length), bytes));
</#if>
}
{
    int length = inputStream.readInt();
    byte[] bytes = new byte[length];
    inputStream.read(bytes);
    ${cm.className}.ResponseParameters params = ${cm.className}.decodeResponse(ClientMessage.createForDecode(new SafeBuffer(bytes), 0));
    <#if cm.responseParams?has_content>
        <#list cm.responseParams as param>
            <#if param.sinceVersionInt lte testForVersion >
                assertTrue(isEqual(<#if param.nullable>null<#else>${convertTypeToSampleValue(param.type)}</#if>, params.${param.name}));
            <#else>
                assertFalse(params.${param.name}Exist);
            </#if>
        </#list>
    </#if>
}
    <#if cm.events?has_content>
{
    class ${cm.className}Handler extends ${cm.className}.AbstractEventHandler {
        <#list cm.events as event >
        @Override
        public void handle(<#if event.eventParams?has_content> <#list event.eventParams as param> <@methodParam type=param.type/> ${param.name} <#if param_has_next>, </#if> </#list> </#if>) {
               <#if event.eventParams?has_content>
                       <#list event.eventParams as param>
                        <#if param.sinceVersionInt lte testForVersion >
                            assertTrue(isEqual(<#if param.nullable>null<#else>${convertTypeToSampleValue(param.type)}</#if>, ${param.name}));
                        </#if>
                       </#list>
                </#if>
        }
        </#list>
    }
    ${cm.className}Handler handler = new ${cm.className}Handler();
    <#list cm.events as event >
    {
        int length = inputStream.readInt();
            byte[] bytes = new byte[length];
            inputStream.read(bytes);
        handler.handle(ClientMessage.createForDecode(new SafeBuffer(bytes), 0));
     }
    </#list>
}
    </#if>
</#if>

</#list>

</#if>
</#list>

        inputStream.close();
        input.close();

    }
}




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
        <#case util.DATA_FULL_NAME>
            <#return "aData">
        <#case "java.lang.String">
            <#return "aString">
        <#case "boolean">
            <#return "boolean">
        <#case "java.util.UUID">
            <#return "aUUID">
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

<#--METHOD PARAM MACRO -->
<#macro methodParam type><#local cat= util.getTypeCategory(type)>
<#switch cat>
<#case "COLLECTION"><#local genericType= util.getGenericType(type)>java.util.Collection<${genericType}><#break>
<#default>${type}
</#switch>
</#macro>