/*
 * Copyright (c) 2008-2019, Hazelcast, Inc. All Rights Reserved.
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

package com.hazelcast.annotation;

import java.lang.annotation.ElementType;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;

/**
 * This annotation is for marking template interfaces to be processed
 */
@Retention(RetentionPolicy.SOURCE)
@Target(ElementType.TYPE)
public @interface GenerateCodec {

    /**
     * Returns master id of class.
     * Mostly id of a distributed object like IMap, IQueue in protocol.
     * This id should be unique.
     * Ids are kept together at com.hazelcast.client.impl.protocol.codec.TemplateConstants
     * to make sure uniqueness.
     *
     * @return id
     */
    short id() default 0;

    /**
     * Suffix to be used when generating request classes.
     *
     * @return name
     */
    String name();

    /**
     * Namespace of related classes in c# client.
     *
     * @return namespace
     */
    String ns();
}
