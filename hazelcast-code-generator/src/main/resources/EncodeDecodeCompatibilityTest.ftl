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

<#include "compatibility-common.ftl">
package com.hazelcast.client.protocol.compatibility;

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
import com.hazelcast.scheduledexecutor.ScheduledTaskHandler;
import com.hazelcast.nio.serialization.Data;
import com.hazelcast.transaction.impl.xa.SerializableXID;

import com.hazelcast.test.HazelcastParallelClassRunner;
import com.hazelcast.test.annotation.ParallelTest;
import com.hazelcast.test.annotation.QuickTest;
import org.junit.experimental.categories.Category;
import org.junit.runner.RunWith;
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

@RunWith(HazelcastParallelClassRunner.class)
@Category({QuickTest.class, ParallelTest.class})
public class EncodeDecodeCompatibilityTest {

    @org.junit.Test
            public void test() {
<#list model?keys as key>
<#assign map=model?values[key_index]?values/>
<#if map?has_content>
<#list map as cm>
{
    ClientMessage clientMessage = ${cm.className}.encodeRequest( <#if cm.requestParams?has_content> <#list cm.requestParams as param>  ${convertTypeToSampleValue(param.type)} <#if param_has_next>, </#if> </#list> </#if>);
    ${cm.className}.RequestParameters params = ${cm.className}.decodeRequest(ClientMessage.createForDecode(clientMessage.buffer(), 0));
    <#if cm.requestParams?has_content>
        <#list cm.requestParams as param>
            assertTrue(isEqual(${convertTypeToSampleValue(param.type)}, params.${param.name}));
        </#list>
    </#if>
}
{
    ClientMessage clientMessage = ${cm.className}.encodeResponse( <#if cm.responseParams?has_content> <#list cm.responseParams as param>  ${convertTypeToSampleValue(param.type)} <#if param_has_next>, </#if> </#list> </#if>);
    ${cm.className}.ResponseParameters params = ${cm.className}.decodeResponse(ClientMessage.createForDecode(clientMessage.buffer(), 0));
    <#if cm.responseParams?has_content>
        <#list cm.responseParams as param>
            assertTrue(isEqual(${convertTypeToSampleValue(param.type)}, params.${param.name}));
        </#list>
    </#if>
}
    <#if cm.events?has_content>
{
    class ${cm.className}Handler extends ${cm.className}.AbstractEventHandler {
        <#list cm.events as event >
        <#assign paramCallList="">
        <#assign assertList="">
        <#assign previousVersion = event.sinceVersion?replace('.','') >
            <#list event.eventParams as p>
                <#if p.versionChanged >
                @Override
                public void  handle${event.name?cap_first}EventV${previousVersion}(${paramCallList}) {
                       ${assertList}
                }
                </#if>
                <#if p_index gt 0 ><#assign paramCallList=paramCallList + ", "></#if>
                <#assign paramCallList += methodParamFnc(p.type) + " " + p.name >
                <#assign assertList+= "\n assertTrue(isEqual("  + convertTypeToSampleValue(p.type) + ","  + p.name + "));" >
                <#assign previousVersion = p.sinceVersion?replace('.','') >
            </#list>
            @Override
            public void  handle${event.name?cap_first}EventV${previousVersion}(${paramCallList}) {
                   ${assertList}
            }
        </#list>
    }
    ${cm.className}Handler handler = new ${cm.className}Handler();
    <#list cm.events as event >
    {
        ClientMessage clientMessage = ${cm.className}.encode${event.name}Event(<#if event.eventParams?has_content> <#list event.eventParams as param>${convertTypeToSampleValue(param.type)} <#if param_has_next>, </#if> </#list> </#if>);
        handler.handle(ClientMessage.createForDecode(clientMessage.buffer(), 0));
     }
    </#list>
}
    </#if>
</#list>
</#if>
</#list>
    }
}

<#--METHOD PARAM MACRO -->
<#macro methodParam type><#local cat= util.getTypeCategory(type)>
<#switch cat>
<#case "COLLECTION"><#local genericType= util.getGenericType(type)>java.util.Collection<${genericType}><#break>
<#default>${type}
</#switch>
</#macro>

<#function methodParamFnc type><#local cat= util.getTypeCategory(type)>
    <#switch cat>
        <#case "COLLECTION">
            <#local genericType= util.getGenericType(type)>
            <#return "java.util.Collection<${genericType}>">
            <#break>
        <#default>
            <#return "${type}">
    </#switch>
</#function>
