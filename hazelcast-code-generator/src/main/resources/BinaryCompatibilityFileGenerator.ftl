<#assign testForVersionString=util.versionAsString(testForVersion)/>
package com.hazelcast.client.protocol.compatibility;

import com.hazelcast.cache.impl.CacheEventData;
import com.hazelcast.cache.impl.CacheEventDataImpl;
import com.hazelcast.cache.impl.CacheEventType;
import com.hazelcast.client.impl.MemberImpl;
import com.hazelcast.client.impl.client.DistributedObjectInfo;
import com.hazelcast.client.impl.protocol.ClientMessage;
import com.hazelcast.client.impl.protocol.codec.*;
import com.hazelcast.core.Member;
import com.hazelcast.internal.serialization.impl.HeapData;
import com.hazelcast.map.impl.SimpleEntryView;
import com.hazelcast.map.impl.querycache.event.DefaultQueryCacheEventData;
import com.hazelcast.map.impl.querycache.event.QueryCacheEventData;
import com.hazelcast.mapreduce.JobPartitionState;
import com.hazelcast.mapreduce.impl.task.JobPartitionStateImpl;
import com.hazelcast.nio.Address;
import com.hazelcast.nio.serialization.Data;
import com.hazelcast.transaction.impl.xa.SerializableXID;

import java.io.DataOutputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.OutputStream;
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
import static com.hazelcast.client.protocol.compatibility.ReferenceObjects.*;


public class BinaryCompatibilityFileGenerator {
    public static void main(String[] args) throws IOException {
        OutputStream out = new FileOutputStream("${testForVersionString}.protocol.compatibility.binary");
        DataOutputStream outputStream = new DataOutputStream(out);
<#list model?keys as key>
<#assign map=model?values[key_index]?values/>
<#if map?has_content>
<#list map as cm>

{
    ClientMessage clientMessage = ${cm.className}.encodeRequest( <#if cm.requestParams?has_content> <#list cm.requestParams as param>  ${convertTypeToSampleValue(param.type)} <#if param_has_next>, </#if> </#list> </#if>);
     outputStream.writeInt(clientMessage.getFrameLength());
     outputStream.write(clientMessage.buffer().byteArray(), 0 , clientMessage.getFrameLength());
}
{
    ClientMessage clientMessage = ${cm.className}.encodeResponse( <#if cm.responseParams?has_content> <#list cm.responseParams as param>  ${convertTypeToSampleValue(param.type)} <#if param_has_next>, </#if> </#list> </#if>);
    outputStream.writeInt(clientMessage.getFrameLength());
    outputStream.write(clientMessage.buffer().byteArray(), 0 , clientMessage.getFrameLength());
}
    <#if cm.events?has_content>
{
    <#list cm.events as event >
    {
        ClientMessage clientMessage = ${cm.className}.encode${event.name}Event(<#if event.eventParams?has_content> <#list event.eventParams as param>${convertTypeToSampleValue(param.type)} <#if param_has_next>, </#if> </#list> </#if>);
        outputStream.writeInt(clientMessage.getFrameLength());
        outputStream.write(clientMessage.buffer().byteArray(), 0 , clientMessage.getFrameLength());
     }
    </#list>
}
    </#if>

</#list>
</#if>
</#list>
         outputStream.close();
         out.close();

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