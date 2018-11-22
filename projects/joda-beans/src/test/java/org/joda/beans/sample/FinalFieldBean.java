/*
 *  Copyright 2001-present Stephen Colebourne
 *
 *  Licensed under the Apache License, Version 2.0 (the "License");
 *  you may not use this file except in compliance with the License.
 *  You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 *  Unless required by applicable law or agreed to in writing, software
 *  distributed under the License is distributed on an "AS IS" BASIS,
 *  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 *  See the License for the specific language governing permissions and
 *  limitations under the License.
 */
package org.joda.beans.sample;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;

import org.joda.beans.Bean;
import org.joda.beans.BeanBuilder;
import org.joda.beans.JodaBeanUtils;
import org.joda.beans.MetaBean;
import org.joda.beans.MetaProperty;
import org.joda.beans.Property;
import org.joda.beans.gen.BeanDefinition;
import org.joda.beans.gen.PropertyDefinition;
import org.joda.beans.impl.direct.DirectBean;
import org.joda.beans.impl.direct.DirectBeanBuilder;
import org.joda.beans.impl.direct.DirectMetaBean;
import org.joda.beans.impl.direct.DirectMetaProperty;
import org.joda.beans.impl.direct.DirectMetaPropertyMap;
import org.joda.beans.impl.flexi.FlexiBean;

/**
 * Mock used for test equals.
 * 
 * @author Stephen Colebourne
 */
@BeanDefinition
public class FinalFieldBean extends DirectBean {

    /**
     * The field that is final.
     */
    @PropertyDefinition
    private final String  fieldFinal;
    /**
     * The field that is not final.
     */
    @PropertyDefinition
    private String fieldNonFinal;
    /**
     * The list that is final.
     */
    @PropertyDefinition
    private final List<String> listFinal = new ArrayList<>();
    /**
     * The flexi that is final.
     */
    @PropertyDefinition
    private final FlexiBean flexiFinal = new FlexiBean();
    /**
     * The person that is final.
     */
    @PropertyDefinition
    private final Person personFinal = new Person();

    /**
     * Creates an instance.
     */
    public FinalFieldBean() {
        this.fieldFinal = null;
    }

    /**
     * Creates an instance.
     * 
     * @param fieldFinal  the final field
     */
    public FinalFieldBean(String fieldFinal) {
        this.fieldFinal = fieldFinal;
    }

    //------------------------- AUTOGENERATED START -------------------------
    /**
     * The meta-bean for {@code FinalFieldBean}.
     * @return the meta-bean, not null
     */
    public static FinalFieldBean.Meta meta() {
        return FinalFieldBean.Meta.INSTANCE;
    }

    static {
        MetaBean.register(FinalFieldBean.Meta.INSTANCE);
    }

    @Override
    public FinalFieldBean.Meta metaBean() {
        return FinalFieldBean.Meta.INSTANCE;
    }

    //-----------------------------------------------------------------------
    /**
     * Gets the field that is final.
     * @return the value of the property
     */
    public String getFieldFinal() {
        return fieldFinal;
    }

    /**
     * Gets the the {@code fieldFinal} property.
     * @return the property, not null
     */
    public final Property<String> fieldFinal() {
        return metaBean().fieldFinal().createProperty(this);
    }

    //-----------------------------------------------------------------------
    /**
     * Gets the field that is not final.
     * @return the value of the property
     */
    public String getFieldNonFinal() {
        return fieldNonFinal;
    }

    /**
     * Sets the field that is not final.
     * @param fieldNonFinal  the new value of the property
     */
    public void setFieldNonFinal(String fieldNonFinal) {
        this.fieldNonFinal = fieldNonFinal;
    }

    /**
     * Gets the the {@code fieldNonFinal} property.
     * @return the property, not null
     */
    public final Property<String> fieldNonFinal() {
        return metaBean().fieldNonFinal().createProperty(this);
    }

    //-----------------------------------------------------------------------
    /**
     * Gets the list that is final.
     * @return the value of the property, not null
     */
    public List<String> getListFinal() {
        return listFinal;
    }

    /**
     * Sets the list that is final.
     * @param listFinal  the new value of the property, not null
     */
    public void setListFinal(List<String> listFinal) {
        JodaBeanUtils.notNull(listFinal, "listFinal");
        this.listFinal.clear();
        this.listFinal.addAll(listFinal);
    }

    /**
     * Gets the the {@code listFinal} property.
     * @return the property, not null
     */
    public final Property<List<String>> listFinal() {
        return metaBean().listFinal().createProperty(this);
    }

    //-----------------------------------------------------------------------
    /**
     * Gets the flexi that is final.
     * @return the value of the property, not null
     */
    public FlexiBean getFlexiFinal() {
        return flexiFinal;
    }

    /**
     * Sets the flexi that is final.
     * @param flexiFinal  the new value of the property, not null
     */
    public void setFlexiFinal(FlexiBean flexiFinal) {
        JodaBeanUtils.notNull(flexiFinal, "flexiFinal");
        this.flexiFinal.clear();
        this.flexiFinal.putAll(flexiFinal);
    }

    /**
     * Gets the the {@code flexiFinal} property.
     * @return the property, not null
     */
    public final Property<FlexiBean> flexiFinal() {
        return metaBean().flexiFinal().createProperty(this);
    }

    //-----------------------------------------------------------------------
    /**
     * Gets the person that is final.
     * @return the value of the property, not null
     */
    public Person getPersonFinal() {
        return personFinal;
    }

    /**
     * Gets the the {@code personFinal} property.
     * @return the property, not null
     */
    public final Property<Person> personFinal() {
        return metaBean().personFinal().createProperty(this);
    }

    //-----------------------------------------------------------------------
    @Override
    public FinalFieldBean clone() {
        return JodaBeanUtils.cloneAlways(this);
    }

    @Override
    public boolean equals(Object obj) {
        if (obj == this) {
            return true;
        }
        if (obj != null && obj.getClass() == this.getClass()) {
            FinalFieldBean other = (FinalFieldBean) obj;
            return JodaBeanUtils.equal(getFieldFinal(), other.getFieldFinal()) &&
                    JodaBeanUtils.equal(getFieldNonFinal(), other.getFieldNonFinal()) &&
                    JodaBeanUtils.equal(getListFinal(), other.getListFinal()) &&
                    JodaBeanUtils.equal(getFlexiFinal(), other.getFlexiFinal()) &&
                    JodaBeanUtils.equal(getPersonFinal(), other.getPersonFinal());
        }
        return false;
    }

    @Override
    public int hashCode() {
        int hash = getClass().hashCode();
        hash = hash * 31 + JodaBeanUtils.hashCode(getFieldFinal());
        hash = hash * 31 + JodaBeanUtils.hashCode(getFieldNonFinal());
        hash = hash * 31 + JodaBeanUtils.hashCode(getListFinal());
        hash = hash * 31 + JodaBeanUtils.hashCode(getFlexiFinal());
        hash = hash * 31 + JodaBeanUtils.hashCode(getPersonFinal());
        return hash;
    }

    @Override
    public String toString() {
        StringBuilder buf = new StringBuilder(192);
        buf.append("FinalFieldBean{");
        int len = buf.length();
        toString(buf);
        if (buf.length() > len) {
            buf.setLength(buf.length() - 2);
        }
        buf.append('}');
        return buf.toString();
    }

    protected void toString(StringBuilder buf) {
        buf.append("fieldFinal").append('=').append(JodaBeanUtils.toString(getFieldFinal())).append(',').append(' ');
        buf.append("fieldNonFinal").append('=').append(JodaBeanUtils.toString(getFieldNonFinal())).append(',').append(' ');
        buf.append("listFinal").append('=').append(JodaBeanUtils.toString(getListFinal())).append(',').append(' ');
        buf.append("flexiFinal").append('=').append(JodaBeanUtils.toString(getFlexiFinal())).append(',').append(' ');
        buf.append("personFinal").append('=').append(JodaBeanUtils.toString(getPersonFinal())).append(',').append(' ');
    }

    //-----------------------------------------------------------------------
    /**
     * The meta-bean for {@code FinalFieldBean}.
     */
    public static class Meta extends DirectMetaBean {
        /**
         * The singleton instance of the meta-bean.
         */
        static final Meta INSTANCE = new Meta();

        /**
         * The meta-property for the {@code fieldFinal} property.
         */
        private final MetaProperty<String> fieldFinal = DirectMetaProperty.ofReadOnly(
                this, "fieldFinal", FinalFieldBean.class, String.class);
        /**
         * The meta-property for the {@code fieldNonFinal} property.
         */
        private final MetaProperty<String> fieldNonFinal = DirectMetaProperty.ofReadWrite(
                this, "fieldNonFinal", FinalFieldBean.class, String.class);
        /**
         * The meta-property for the {@code listFinal} property.
         */
        @SuppressWarnings({"unchecked", "rawtypes" })
        private final MetaProperty<List<String>> listFinal = DirectMetaProperty.ofReadWrite(
                this, "listFinal", FinalFieldBean.class, (Class) List.class);
        /**
         * The meta-property for the {@code flexiFinal} property.
         */
        private final MetaProperty<FlexiBean> flexiFinal = DirectMetaProperty.ofReadWrite(
                this, "flexiFinal", FinalFieldBean.class, FlexiBean.class);
        /**
         * The meta-property for the {@code personFinal} property.
         */
        private final MetaProperty<Person> personFinal = DirectMetaProperty.ofReadOnly(
                this, "personFinal", FinalFieldBean.class, Person.class);
        /**
         * The meta-properties.
         */
        private final Map<String, MetaProperty<?>> metaPropertyMap$ = new DirectMetaPropertyMap(
                this, null,
                "fieldFinal",
                "fieldNonFinal",
                "listFinal",
                "flexiFinal",
                "personFinal");

        /**
         * Restricted constructor.
         */
        protected Meta() {
        }

        @Override
        protected MetaProperty<?> metaPropertyGet(String propertyName) {
            switch (propertyName.hashCode()) {
                case 553434268:  // fieldFinal
                    return fieldFinal;
                case 1043548611:  // fieldNonFinal
                    return fieldNonFinal;
                case -1247489160:  // listFinal
                    return listFinal;
                case 1629293510:  // flexiFinal
                    return flexiFinal;
                case -448986335:  // personFinal
                    return personFinal;
            }
            return super.metaPropertyGet(propertyName);
        }

        @Override
        public BeanBuilder<? extends FinalFieldBean> builder() {
            return new DirectBeanBuilder<>(new FinalFieldBean());
        }

        @Override
        public Class<? extends FinalFieldBean> beanType() {
            return FinalFieldBean.class;
        }

        @Override
        public Map<String, MetaProperty<?>> metaPropertyMap() {
            return metaPropertyMap$;
        }

        //-----------------------------------------------------------------------
        /**
         * The meta-property for the {@code fieldFinal} property.
         * @return the meta-property, not null
         */
        public final MetaProperty<String> fieldFinal() {
            return fieldFinal;
        }

        /**
         * The meta-property for the {@code fieldNonFinal} property.
         * @return the meta-property, not null
         */
        public final MetaProperty<String> fieldNonFinal() {
            return fieldNonFinal;
        }

        /**
         * The meta-property for the {@code listFinal} property.
         * @return the meta-property, not null
         */
        public final MetaProperty<List<String>> listFinal() {
            return listFinal;
        }

        /**
         * The meta-property for the {@code flexiFinal} property.
         * @return the meta-property, not null
         */
        public final MetaProperty<FlexiBean> flexiFinal() {
            return flexiFinal;
        }

        /**
         * The meta-property for the {@code personFinal} property.
         * @return the meta-property, not null
         */
        public final MetaProperty<Person> personFinal() {
            return personFinal;
        }

        //-----------------------------------------------------------------------
        @Override
        protected Object propertyGet(Bean bean, String propertyName, boolean quiet) {
            switch (propertyName.hashCode()) {
                case 553434268:  // fieldFinal
                    return ((FinalFieldBean) bean).getFieldFinal();
                case 1043548611:  // fieldNonFinal
                    return ((FinalFieldBean) bean).getFieldNonFinal();
                case -1247489160:  // listFinal
                    return ((FinalFieldBean) bean).getListFinal();
                case 1629293510:  // flexiFinal
                    return ((FinalFieldBean) bean).getFlexiFinal();
                case -448986335:  // personFinal
                    return ((FinalFieldBean) bean).getPersonFinal();
            }
            return super.propertyGet(bean, propertyName, quiet);
        }

        @SuppressWarnings("unchecked")
        @Override
        protected void propertySet(Bean bean, String propertyName, Object newValue, boolean quiet) {
            switch (propertyName.hashCode()) {
                case 553434268:  // fieldFinal
                    if (quiet) {
                        return;
                    }
                    throw new UnsupportedOperationException("Property cannot be written: fieldFinal");
                case 1043548611:  // fieldNonFinal
                    ((FinalFieldBean) bean).setFieldNonFinal((String) newValue);
                    return;
                case -1247489160:  // listFinal
                    ((FinalFieldBean) bean).setListFinal((List<String>) newValue);
                    return;
                case 1629293510:  // flexiFinal
                    ((FinalFieldBean) bean).setFlexiFinal((FlexiBean) newValue);
                    return;
                case -448986335:  // personFinal
                    if (quiet) {
                        return;
                    }
                    throw new UnsupportedOperationException("Property cannot be written: personFinal");
            }
            super.propertySet(bean, propertyName, newValue, quiet);
        }

        @Override
        protected void validate(Bean bean) {
            JodaBeanUtils.notNull(((FinalFieldBean) bean).listFinal, "listFinal");
            JodaBeanUtils.notNull(((FinalFieldBean) bean).flexiFinal, "flexiFinal");
            JodaBeanUtils.notNull(((FinalFieldBean) bean).personFinal, "personFinal");
        }

    }

    //-------------------------- AUTOGENERATED END --------------------------
}
